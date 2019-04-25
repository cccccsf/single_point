#!/usr/bin/python3
import os
import shutil
from OsComponents import mkdir


def copy_inp_file(job):
    ziel_path = job.path
    if not os.path.exists(ziel_path):
        mkdir(ziel_path)
    inp_path = os.path.dirname(__file__)
    inp_from = os.path.join(inp_path, 'input.loc')
    inp_to = os.path.join(ziel_path, 'input.loc')
    shutil.copy(inp_from, inp_to)
    print(ziel_path)
    print('input.loc copied.')
