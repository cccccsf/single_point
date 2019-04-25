#!/usr/bin/python3
import re
from Components import cal_layer_energy
from Components import record_data_json
from Components import record_data_csv
from OsComponents import record


def get_energy(job):
    path = job.path
    f = open(path + '/hf.out', 'r')
    lines = f.read()
    # lines = ' '.join(lines.split()) + '#'
    f.close()

    regex = 'CYC   0.*?\n'
    energy_block = re.search(regex, lines).group(0)    # CYC   0 ETOT(AU) -2.726040216969E+03 DETOT -2.73E+03 tst  0.00E+00 PX  1.00E+00
    regex_2 = r'ETOT\(AU\) .*? '
    energy_block = re.search(regex_2, energy_block).group(0)    # ETOT(AU) -2.726040216969E+03
    unit = search_unit(energy_block)
    energy_block = energy_block.strip()
    energy_block = energy_block.split(' ')
    energy = energy_block[-1]   # str

    return energy, unit


def search_unit(energy_block):
    reg = r'\(.*?\)'
    unit_block = re.search(reg, energy_block)
    if unit_block is not None:
        unit_block = unit_block.group(0)
        unit = unit_block[1:-1]
        if unit == 'AU':
            unit = 'hartree'
    else:
        unit = 'default'
    return unit


def read_record_results(path, jobs):
    energy_dict = {}
    for job in jobs:
        if job.layertype == 'bilayer':
            energy, unit = get_energy(job)
            energy = [energy, unit]
            energy_dict['bilayer'] = energy
        elif job.layertype == 'upperlayer':
            energy, unit = get_energy(job)
            energy = [energy, unit]
            energy_dict['upperlayer'] = energy
        elif job.layertype == 'underlayer':
            energy, unit = get_energy(job)
            energy = [energy, unit]
            energy_dict['underlayer'] = energy
    layer_energy = cal_layer_energy(
        energy_dict['bilayer'],
        energy_dict['upperlayer'],
        energy_dict['underlayer'])
    energy_dict['layer_energy'] = layer_energy
    record_data_json(path, 'energy', energy_dict, section='hf2')
    record_data_csv(path,
                    'hf2',
                    [energy_dict['bilayer'][0],
                     energy_dict['upperlayer'][0],
                        energy_dict['underlayer'][0],
                        energy_dict['layer_energy'][0]],
                    layer='whole layer')
    rec = 'Results readed.\n'
    rec += '---' * 25
    print(rec)
    record(path, rec)


if __name__ == '__main__':

    from Components import Job

    def test_get_energy():
        path = r'C:\Users\ccccc\Documents\Theoritische Chemie\Masterarbeit\test\hf_2\x_-0.150\z_-0.106'
        job = Job(path)
        energy, unit = get_energy(job)
        print(energy, unit)
        expected = '-2.726040216969E+03'
        assert(energy == expected)

    test_get_energy()


