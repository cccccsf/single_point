#!/usr/bin/python3
import os
import sys
import shutil
from Components import IniReader
from Components import record_data_json
from Components import Job
from OsComponents import record
import Correction


def correction(path):

    rec = 'Correction begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    Ini = IniReader()
    project_name, *_ = Ini.get_basic_info()
    nodes, memorys, bs, molpro_path, molpro_key, atoms = Ini.get_correction()
    record_data_json(path, 'memorys', memorys, section='correction')
    record_data_json(path, 'nodes', nodes, section='correction')
    # prepare input
    cluster_path = os.path.join(path, 'cluster')
    missions, nodes, memorys = get_missions(memorys, nodes)

    # prepare input
    inputs = list(missions)
    inputs = [inp + '.inp' for inp in inputs]
    inputs_files = [os.path.join(cluster_path, inp) for inp in inputs]
    correction_jobs = []
    correction_jobs_finished = []
    for inp in inputs_files:
        inp_inp = os.path.join(path, os.path.split(inp)[-1])
        job = Job(cluster_path)
        job.method = os.path.split(inp)[-1].split('.')[0]
        job.input = inp
        if not Correction.if_cal_finish(job):
            correction_jobs.append(job)
            if not os.path.exists(inp) and not os.path.exists(inp_inp):
                print('{} file not found.'.format(inp))
                print('Program will generate the input automatically.')
                if job.method.startswith('per'):
                    Inp = Correction.InputPerRPA(job, project_name, memorys[job.method], uc_atoms=atoms)
                    Inp.gen_inp()
                elif job.method.endswith('rpa_cc'):
                    Inp = Correction.InputRPACC(job, project_name, memorys[job.method], uc_atoms=atoms)
                    Inp.gen_inp()
                elif job.method.endswith('iext1_rpa'):
                    Inp = Correction.InputIext1RPA(job, project_name, memorys[job.method], uc_atoms=atoms)
                    Inp.gen_inp()
            elif not os.path.exists(inp):
                shutil.copy(inp_inp, inp)

        else:
            job.status = 'finished'
            correction_jobs_finished.append(job)

    # generate scr
    for job in correction_jobs:
        Src = Correction.Script(job, nodes[job.method], molpro_key, molpro_path)
        Src.write_scr()

    # submit jobs
    if len(correction_jobs) > 0:
        new_finished_jobs = Correction.submit(correction_jobs)
        correction_jobs_finished += new_finished_jobs

    # read and record all results
    if len(correction_jobs_finished) > 0:
        Correction.read_all_results(path, correction_jobs_finished)

    rec = 'Correction finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)


yes_or_no = {
    'Y': 1,
    'y': 1,
    'Yes': 1,
    'yes': 1,
    'N': 0,
    'n': 0,
    'No': 0,
    'no': 0}


def get_missions(memorys, nodes):
    missions_nodes = {key for key in nodes.keys()}
    missions_memory = {key for key in memorys.keys()}
    missions = missions_memory | missions_nodes
    for m in missions:
        if m not in missions_nodes:
            print('nodes info of job {} not found!'.format(m))
            print('Do you want to use the default value 12? Please enter y(es)/n(o)...')
            default = input()
            default = yes_or_no[default]
            if default == 1:
                nodes[m] = 12
            else:
                print('Please correct the info and restart the programm.')
                print('Program exits...')
                sys.exit()
        if m not in missions_memory:
            print('memory info of job {} not found!'.format(m))
            print(
                'Do you want to use the default value 2000 M ? Please enter y(es)/n(o)...')
            default = input()
            default = yes_or_no[default]
            if default == 1:
                memorys[m] = 2000
            else:
                print('Please correct the info and restart the programm.')
                print('Program exits...')
                sys.exit()
    return missions, nodes, memorys


def compare_inp_files(path, inputs, nodes, memorys):
    walks = os.walk(path)
    for root, dirs, files in walks:
        if root == path:
            f = files
    files = [i for i in f if i.endswith('.inp')]
    for f in files:
        if f not in inputs:
            print(f, ';  job info not include in ini file.')
            print('Do you want to use default setting to calculate?')
            print('Please enter y(es)/n(o)...')
            default = input()
            # default = 'y'
            default = yes_or_no[default]
            if default == 1:
                nodes[f.split('.')[0]] = 12
                memorys[f.split('.')[0]] = 2000
            else:
                print(
                    'Please add the info in ini file or delete needless input file and restart the programm.')
                print('Programm exits...')
                sys.exit()
    return inputs, nodes, memorys


def check_inp_files(inputs_files):
    for inp in inputs_files:
        if not os.path.exists(inp):
            return False
    return True
