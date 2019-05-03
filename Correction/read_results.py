#!/usr/bin/python3
import os
import re
from Components import record_data_json
from Components import record_data_csv
from OsComponents import record
from Components import is_number


class Result(object):

    def __init__(self, job, unit_type='Hartree'):
        self.job = job
        self.path = job.path
        self.method = job.method
        self.step = self.get_step()
        self.bs = self.get_bs_type()
        self.energy, self.unit = None, None
        self.unit_type = unit_type

    def get_method_error(self):
        out_file = os.path.join(self.path, self.job.method) + '.out'
        with open(out_file, 'rb') as f:
            f.seek(-20000, 2)
            text = f.read().decode('utf-8')
        pattern = 'DELTA_DE_LCCSDT_RPA.*?\n'
        energy = re.search(pattern, text)
        if energy is not None:
            energy = energy.group(0)
            energy = energy.strip()
            energy = energy.split()
            if is_number(energy[-1]):
                unit = 'Hartree'
                energy = float(energy[-1])
            elif is_number(energy[-2]):
                unit = energy[-1].lower()
                energy = float(energy[-2])
            else:
                print(self.job)
                print('Energy infomation not found...')
                print('Please check the output file.')
                energy, unit = None, None
        else:
            print(self.job)
            print('Energy infomation not found...')
            print('Please check the output file.')
            unit = None
        return energy, unit

    def get_step(self):
        step = self.method.split('_')
        step = step[1:]
        step = '_'.join(step)
        return step

    def get_bs_type(self):
        bs = self.method.split('_')[0]
        bs_set = {'avdz', 'avtz', 'avqz'}
        assert bs in bs_set or bs == 'per'
        return bs

    def get_e_iext1_rpa(self):
        out_file = os.path.join(self.path, self.job.method) + '.out'
        with open(out_file, 'rb') as f:
            f.seek(-20000, 2)
            text = f.read().decode('utf-8')
        pattern = 'DE_LRPA.*?\n'
        unit = None
        energy = re.search(pattern, text)
        if energy is not None:
            energy = energy.group(0)
            energy = energy.strip()
            energy = energy.split()
            if is_number(energy[-1]):
                unit = 'Hartree'
                energy = float(energy[-1])
            elif is_number(energy[-2]):
                unit = energy[-1].lower()
                energy = float(energy[-2])
            else:
                print(self.job)
                print('Energy infomation not found...')
                print('Please check the output file.')
                energy = None
        else:
            print(self.job)
            print('Energy infomation not found...')
            print('Please check the output file.')
        return energy, unit

    def get_energy(self):
        if self.step == 'rpa_cc':
            self.energy, self.unit = self.get_method_error()
        else:
            self.energy, self.unit = self.get_e_iext1_rpa()

    def unit_transform(self):
        unit_dict = {
            'ha': 1,
            'hartree': 1,
            'ev': 27.2113839,
            'cm': 219474.63067,
            'kcal/mol': 627.5096,
            'kj/mol': 2625.50,
            'k': 3.157747E5,
            'hz': 6.5796839207E15
        }
        self.unit_type = self.unit_type.lower()
        if self.unit is None:
            print(self.job, ':')
            print('unit not Found.')
        elif self.unit.lower() not in unit_dict or self.unit_type not in unit_dict:
            print(self.job, ':')
            print('unit not found in our unit dictionary.')
            print('unit transform will not continue.')
        else:
            unit_from = unit_dict[self.unit]
            unit_to = unit_dict[self.unit_type]
            coe = unit_to / unit_from
            self.energy = self.energy * coe
            self.unit = self.unit_type


def read_all_results(path, jobs):
    Results = [Result(job) for job in jobs]
    for res in Results:
        res.get_energy()
        res.unit_transform()
    energy_dict = {res.method: [res.energy, res.unit] for res in Results}
    record_data_json(path, 'energy', energy_dict, section='correction')
    for res in Results:
        record_data_csv(path, res.method, res.energy, layer='interlayer')
    rec = 'Results readed.\n'
    rec += '---' * 25
    print(rec)
    record(path, rec)


if __name__ == '__main__':
    from Components import Job
    path = r'C:\Users\ccccc\PycharmProjects\single_point\test\cluster'
    job = Job(path)
    job.method = 'per_bas_rpa_iext1'
    inp = os.path.join(path, 'per_bas_rpa_iext1.inp')
    job.input = inp
    Res = Result(job)
    Res.get_energy()
    print(Res.energy)
