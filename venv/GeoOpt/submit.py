#!/usr/bin/python3
import os
import re
import subprocess
import shutil
import time
import datetime
import GeoOpt
from OsComponents import record
from OsComponents import rename_file
from Components import Job



def submit_geo_opt_job():
    chmod = 'chmod u+x geo_opt'
    command = 'qsub geo_opt'
    try:
        subprocess.call(chmod, shell=True)
    except:
        pass
    try:
        out_bytes = subprocess.check_output(['qsub', 'geo_opt'])
    except subprocess.CalledProcessError as e:
        out_bytes = e.output
        code = e.returncode
        print(code)
    except FileNotFoundError as e:
        print(e)
        print('Windows Test.')
        out_text = '*****.rigi'
        return out_text
    out_text = out_bytes.decode('utf-8')
    out_text = out_text.strip('\n')
    return out_text

def update_nodes(path, nodes, crystal_path):
    scr = os.path.join(path, 'geo_opt')
    with open(scr, 'r') as f:
        lines = f.readlines()
    nodes_line = lines[3]
    loc = 3
    if nodes_line.startswith('#PBS -l nodes'):
        pass
    else:
        i = 0
        for line in lines:
            if line.startswith('#PBS -l nodes'):
                nodes_line = line
                loc = i
            i += 1
    loc2, loc_cry = 0, 0
    j = 0
    for line in lines:
        if line.startswith('mpirun -np'):
            loc2 = j
        if line.startswith('crystal_path='):
            loc_cry = j
        j += 1
    if nodes != '':
        nodes_line = '#PBS -l nodes={}\n'.format(nodes)
        lines[loc] = nodes_line
        lines[loc2] = 'mpirun -np {} $crystal_path/Pcrystal >& ${{PBS_O_WORKDIR}}/geo_opt.out\n'.format(nodes)
    if crystal_path != '':
        lines[loc_cry] = 'crystal_path={}\n'.format(crystal_path)

    with open(scr, 'w') as f:
        f.writelines(lines)

def copy_submit_scr(job, nodes, crystal_path):
    ziel_path = job.path
    scr_path = os.path.dirname(os.path.realpath(__file__))
    scr_from = os.path.join(scr_path, 'job_submit.bash')
    scr_to = os.path.join(ziel_path, 'geo_opt')
    shutil.copy(scr_from, scr_to)
    update_nodes(ziel_path, nodes, crystal_path)
    print('Submition file copied.')


def submit(job, nodes, crystal_path, path):

    if not GeoOpt.if_job_finish(job):
        copy_submit_scr(job, nodes, crystal_path)
        rename_file(job.path, 'geo_opt.out')
        out = submit_geo_opt_job()
        rec = job.path
        rec += '\n'
        rec += 'job submitted...'
        rec += '\n' + out + '\n'
        rec += '---'*25
        print(rec)
        record(path, rec)
        r = 0
        while True:
           if GeoOpt.if_job_finish(job):
               rec = 'calculation finished.\n'
               rec += '---'*25
               print(rec)
               record(path, rec)
               job.status = 'finished'
               break
           else:
               time.sleep(500)
               r += 1
               if r > 15:
                   rec = 'calculation still not finished.\n'
                   rec += '---'*25
                   print(rec)
                   record(path, rec)
                   r = 0
               continue
    else:
        job.status = 'finished'

    return job
