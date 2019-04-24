#!/usr/bin/python3
import os
import re
import csv
from Components import record_data_json
from Components import record_data_csv
from OsComponents import record


def get_optimized_geometry(out_file):

    with open(out_file, 'r') as f:
        lines = f.read().replace('\n', ':')
    lines = ' '.join(lines.split()) + '#'

    # search geometry infomation
    regex = 'FINAL OPTIMIZED GEOMETRY.*GEOMETRY OUTPUT FILE'
    geo_block = re.search(regex, lines).group(0)
    regex_2 = 'LATTICE PARAMETERS.*'
    lattice_block = re.search(regex_2, geo_block).group(0)
    lattice_block = re.split(':', lattice_block.replace(': ', ':'))

    i = 0
    sep = []
    for l in lattice_block:
        if l == '*******************************************************************************':
            sep.append(i)
        i += 1

    lattice_parameter = lattice_block[sep[0] - 1]
    lattice_parameter = lattice_parameter.split()

    geometry = []
    j = 1
    for l in lattice_block[9:]:
        if len(l) > 3 and l[0] == str(j):
            geometry.append(l)
            j += 1
    geometry_split = []
    for geo in geometry:
        geometry_split.append(geo.split())
    for geo in geometry_split:
        del geo[0]
        del geo[0]
        del geo[1]

    return lattice_parameter, geometry_split


def get_optimized_energy(out_file):
    with open(out_file, 'r') as f:
        lines = f.read()
    lines = ' '.join(lines.split()) + '#'
    regex = 'OPT END.* POINTS'
    energy_block = re.search(regex, lines).group(0)
    unit = search_unit(energy_block)
    regex_2 = ': .* '
    energy_block = re.search(regex_2, energy_block).group(0)
    energy = energy_block[2:-1]
    return energy, unit


def search_unit(energy_block):
    reg = '\(.*?\)'
    unit_block = re.search(reg, energy_block)
    if unit_block is not None:
        unit_block = unit_block.group(0)
        unit = unit_block[1:-1]
        if unit == 'AU':
            unit = 'hartree'
    else:
        unit = 'default'
    return unit


def creatxls_dis(path):
    csv_path = os.path.join(path, 'result.csv')
    headers = ['displacement', 'distance(A)', 'E(au)']
    with open(csv_path, 'w', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)


def read_record_result(job, path):
    job_path = job.path
    out_file = os.path.join(job_path, 'geo_opt.out')
    lattice_parameter, geometry = get_optimized_geometry(out_file)
    energy, unit = get_optimized_energy(out_file)
    record_data_json(path, 'unit', unit, section='geo_opt')
    record_data_json(path, 'optimized_lattice_parameter', lattice_parameter, section='geo_opt')
    record_data_json(path, 'optimized_geometry', geometry, section='geo_opt')
    record_data_json(path, 'energy', energy, section='geo_opt')
    record_data_csv(path, 'geo_opt', energy)
    rec = job.path + '\n'
    rec += 'Output Info readed.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)


if __name__ == '__main__':
    outfile = r'C:\Users\ccccc\PycharmProjects\single_point\test\geo_opt\geo_opt.out'
    energy = get_optimized_energy(outfile)
