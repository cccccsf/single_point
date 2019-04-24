#!/usr/bin/python3
import os
import subprocess
import shutil
import time
from HF1 import if_cal_finish
from OsComponents import rename_file
from OsComponents import record


def submit_hf1_job():
    chmod = 'chmod u+x hf'
    try:
        subprocess.call(chmod, shell=True)
    except:
        pass
    try:
        out_bytes = subprocess.check_output(['qsub', 'hf'])
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


def copy_submit_scr(job, nodes, crystal_path):
    ziel_path = job.path
    scr_path = os.path.dirname(os.path.realpath(__file__))
    scr_from = os.path.join(scr_path, 'job_submit.bash')
    scr_to = os.path.join(ziel_path, 'hf')
    shutil.copy(scr_from, scr_to)
    update_nodes(ziel_path, nodes, crystal_path)
    print('Submition file copied...')


def update_nodes(path, nodes, crystal_path):
    scr = os.path.join(path, 'hf')
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
        lines[loc2] = 'mpirun -np {} $crystal_path/Pcrystal >& ${{PBS_O_WORKDIR}}/hf.out\n'.format(nodes)
    if crystal_path != '':
        lines[loc_cry] = 'crystal_path={}\n'.format(crystal_path)

    with open(scr, 'w') as f:
        f.writelines(lines)


def submit(jobs):
    job_num = len(jobs)
    max_paralell = 3
    count = 0
    submitted_jobs = []
    finished_jobs = []

    def test_finished(jobs):
        nonlocal count
        for job in jobs[:]:
            if if_cal_finish(job):
                finished_jobs.append(job)
                rec = job.path
                rec += '\n'
                rec += 'calculation finished...'
                rec += '---'*25
                print(rec)
                record(job.root_path, rec)
                count -= 1
                jobs.remove(job)

    #test if there is some job which is already finished
    for job in jobs[:]:
        #print(job)
        if if_cal_finish(job):
            finished_jobs.append(job)
            jobs.remove(job)

    #submit and detect statu of jobs
    j = 0
    while True:
        test_finished(submitted_jobs)
        if len(finished_jobs) == job_num and len(submitted_jobs) == 0:
            break
        else:
            if count < max_paralell and len(jobs) != 0:
                new_job = jobs.pop()
                os.chdir(new_job.path)
                rename_file(new_job.path, 'hf.out')
                rename_file(new_job.path, 'fort.9')
                out = submit_hf1_job()
                count += 1
                submitted_jobs.append(new_job)
                rec = new_job.path + '\n'
                rec += 'job submitted...'
                rec += '\n' + out + '\n'
                rec += '---'*25
                record(new_job.root_path, rec)
            else:
                time.sleep(500)
                j += 1
                if j > 15:
                    rec = 'noting changes...'
                    record(submitted_jobs[0].root_path, rec)
                    j = 0
                continue

    return finished_jobs
