#!/usr/bin/python3
import os
from Components import IniReader
from Components import record_data_json
from Components import Job
from OsComponents import record
import LMP2


def lmp2(path):

    rec = 'LMP2 Calculation begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    ini = IniReader()
    nodes, cryscor_path = ini.get_lmp2()
    record_data_json(path, 'nodes', nodes, section='lmp2')

    # generation of INPUT
    bilayer_path = os.path.join(path, 'lmp2')
    upper_path = os.path.join(bilayer_path, 'upperlayer')
    under_path = os.path.join(bilayer_path, 'underlayer')
    bilayer_job = Job(bilayer_path)
    upper_job = Job(upper_path)
    under_job = Job(under_path)
    lmp2_jobs_finished, lmp2_jobs_new = [], []
    if not LMP2.if_cal_finish(bilayer_job):
        inp = LMP2.Lmp2Input(bilayer_job)
        inp.write_input()
        lmp2_jobs_new.append(bilayer_job)
        LMP2.copy_submit_src(bilayer_job, nodes, cryscor_path)
    else:
        bilayer_job.status = 'finished'
        lmp2_jobs_finished.append(bilayer_job)
    if not LMP2.if_cal_finish(upper_job):
        inp = LMP2.Lmp2InputLayer(upper_job)
        inp.write_input()
        lmp2_jobs_new.append(upper_job)
        LMP2.copy_submit_src(upper_job, nodes, cryscor_path)
    else:
        upper_job.status = 'finished'
        lmp2_jobs_finished.append(upper_job)
    if not LMP2.if_cal_finish(under_job):
        inp = LMP2.Lmp2InputLayer(under_job)
        inp.write_input()
        lmp2_jobs_new.append(under_job)
        LMP2.copy_submit_src(under_job, nodes, cryscor_path)
    else:
        under_job.status = 'finished'
        lmp2_jobs_finished.append(under_job)

    # submit jobs
    if len(lmp2_jobs_new) > 0:
        new_finished_jobs = LMP2.submit(lmp2_jobs_new)
        lmp2_jobs_finished += new_finished_jobs

    # read and record results
    LMP2.lmp2_read_record_results(path, lmp2_jobs_finished)

    rec = 'LMP2 finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)
