#!/usr/bin/python3
import os
import shutil
import time
from OsComponents import record
from OsComponents import submit_job
from LMP2 import if_cal_finish


def copy_fort80(ziel_path):
    original_path = ziel_path.replace('lmp2', 'loc')
    try:
        fort80_to = os.path.join(ziel_path, 'fort.80')
        fort80_from = os.path.join(original_path, 'fort.80')
        shutil.copy(fort80_from, fort80_to)
        print('fort.80 copied.')
    except Exception as e:
        print(e)
        print('fort.80 failed to copy.')


def copy_fort9_fort78(ziel_path):
    original_path = ziel_path.replace('lmp2', 'hf2')
    try:
        fort9_from = os.path.join(original_path, 'fort.9')
        fort9_to = os.path.join(ziel_path, 'fort.9')
        fort78_from = os.path.join(original_path, 'fort.78')
        fort78_to = os.path.join(ziel_path, 'fort.78')
        shutil.copy(fort9_from, fort9_to)
        shutil.copy(fort78_from, fort78_to)
        print('fort.9 and fort.78 copied.')
    except Exception as e:
        print(e)
        print('fort.9 and fort.78 failed to copy.')


def copy_submit_src(job, nodes, cryscor_path):
    ziel_path = job.path
    scr_path = os.path.dirname(__file__)
    scr_from = os.path.join(scr_path, 'job_submit_lmp2.bash')
    scr_to = os.path.join(ziel_path, 'lmp2')
    try:
        shutil.copy(scr_from, scr_to)
        update_scr(job, nodes, cryscor_path)
        print('Submition file copied.')
    except Exception as e:
        print(e)
        print('submit scr failed to copy.')


def update_scr(job, nodes, cryscor_path):
    path = job.path
    scr = os.path.join(path, 'lmp2')
    with open(scr, 'r') as f:
        lines = f.readlines()

    # update nodes
    nodes_line = lines[3]
    loc = 3
    if nodes_line.startswith('#PBS -l nodes'):
        pass
    else:
        i = 0
        for line in lines:
            if line.startswith('#PBS -l nodes'):
                loc = i
            i += 1
    if nodes != '' and nodes != 'default':
        nodes_line = '#PBS -l nodes={}'.format(nodes)
        lines[loc] = nodes_line

    # update cryscor path and currdir
    loc_cry, loc_curr, i = 0, 0, 0
    for line in lines:
        if line.startswith('cryscor_path'):
            loc_cry = i
        if line.startswith('currdir='):
            loc_curr = i
        i += 1
    if cryscor_path != '':
        cryscor_line = 'cryscor_path={}\n'.format(cryscor_path)
        lines[loc_cry] = cryscor_line
    if job.layertype == 'bilayer':
        currdir_line = 'currdir=/scratch/$USER/lmp2/{}/{}\n'.format(job.x_dirname, job.z_dirname)
    else:
        currdir_line = 'currdir=/scratch/$USER/lmp2/{}/{}/{}\n'.format(job.x_dirname, job.z_dirname, job.layertype)
    lines[loc_curr] = currdir_line

    with open(scr, 'w') as f:
        f.writelines(lines)


def submit(jobs):
    job_num = len(jobs)
    max_paralell = 12
    count = 0
    submitted_jobs = []
    finished_jobs = []

    def test_finished(jobs):
        """
        test jobs which have benn submittdt is finished or not
        if a job finished, add it to list finished_jobs, and delete it from list submitted_jobs
        :param submitted_jobs:
        :return:
        """
        nonlocal count
        for job in jobs[:]:
            if if_cal_finish(job):
                finished_jobs.append(job)
                rec = job.path
                rec += '\n'
                rec += 'calculation finished...\n'
                rec += '---'*25
                print(rec)
                record(job.root_path, rec)
                jobs.remove(job)
                count -= 1

    # test if there is some job which is already finished
    for job in jobs[:]:
        if if_cal_finish(job):
            finished_jobs.append(job)
            jobs.remove(job)

    # submit and detect all jobs
    j = 0
    while True:
        test_finished(submitted_jobs)   # update list finished_jobs and list submitted_jobs
        if len(finished_jobs) == job_num and len(submitted_jobs) == 0:
            break
        else:
            if count <= max_paralell and len(jobs) > 0:       # check the number of jobs which is running now
                new_job = jobs.pop()
                copy_fort80(new_job.path)
                copy_fort9_fort78(new_job.path)
                out = submit_job(new_job, 'lmp2')
                count += 1
                submitted_jobs.append(new_job)
                rec = new_job.path + '\n'
                rec += 'job submitted.'
                rec += '\n' + out + '\n'
                rec += '---'*25
                record(new_job.root_path, rec)
                print(rec)
            else:
                time.sleep(500)
                j += 1
                if j > 15:
                    rec = 'noting changes.'
                    record(submitted_jobs[0].root_path, rec)
                    j = 0
                continue

    return finished_jobs

