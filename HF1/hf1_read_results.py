#!/usr/bin/python3
import re
from Components import cal_layer_energy
from Components import record_data_json
from Components import record_data_csv
from OsComponents import record


def if_converged(energy_block):
    regex = '- .*?E\('
    try:
        status = re.search(regex, energy_block).group(0)
        status = status[2:-3]
        if status == 'CONVERGENCE ON ENERGY':
            return True
        elif status == 'TOO MANY CYCLES':
            return False
        else:
            print('---' * 15)
            print(path)
            print('Status not found.')
            print('Please check the output file.')
            return False
    except AttributeError as e:
        print('---' * 15)
        print(path)
        print('Status not found.')
        print('Please check the output file.')


def get_energy(job):
    path = job.path
    f = open(path + '/hf.out', 'r')
    lines = f.read()
    lines = ' '.join(lines.split()) + '#'
    f.close()
    energy = 'Nah'
    unit = 'Nah'

    # regex = 'SCF ENDED - CONVERGENCE ON ENERGY .* CYCLES'
    regex = 'SCF ENDED .* CYCLES'
    try:
        # SCF ENDED - CONVERGENCE ON ENERGY E(AU) -2.7260361085525E+03 CYCLES
        energy_block = re.search(regex, lines).group(0)
        status = if_converged(energy_block)
        if status is True:
            regex_2 = r'E\(AU\) .* '
            energy_block = re.search(regex_2, energy_block).group(
                0)  # E(AU) -2.7260361085525E+03
            unit = search_unit(energy_block)
            regex_3 = ' .* '
            energy_block = re.search(regex_3, energy_block).group(
                0)    # -2.7260361085525E+03
            energy = energy_block[1:-1]    # str
            job.set_status('finished')
        else:
            print('---' * 15)
            print(job)
            print('Calculation not converged.')
            print(
                'Please check the output file and change some parameters to recalculate the job.')
            job.set_status('not converged')
    except AttributeError as e:
        print('---' * 15)
        print(job)
        print('Energy not found.')
        print('Please check the output file.')
        job.set_status('error')

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
    record_data_json(path, 'energy', energy_dict, section='hf1')
    record_data_csv(path,
                    'hf1',
                    [energy_dict['bilayer'][0],
                     energy_dict['upperlayer'][0],
                        energy_dict['underlayer'][0],
                        energy_dict['layer_energy'][0]],
                    layer='whole layer')
    rec = 'Results readed.\n'
    rec += '---' * 25
    print(rec)
    record(path, rec)
