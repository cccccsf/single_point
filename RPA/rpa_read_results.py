#!/usr/bin/python3
import os
import re


def get_energy(job):

    path = job.path
    path = os.path.join(path, 'rpa.out')
    with open(path, 'rb') as f:
        f.seek(-20000, 2)
        lines = f.read().decode('utf-8')
    regex = 'LRPA correlation energy.*?\n'
    energy = re.search(regex, lines, re.M|re.S)
    if energy is not None:
        energy = energy.group(0)
    else:
        print(path)
        print('Energy information not found...')

    energy = energy.strip()
    energy = energy.split()
    energy = energy[-1]
    unit = 'hartree'    # here need more info

    return energy, unit
