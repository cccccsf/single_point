#!/usr/bin/python3
import os
from Components import IniReader
from Components import Job
from Components import read_record_results
from OsComponents import record
import RPA


def rpa(path):

    rec = 'LRPA begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    ini = IniReader()
    rpa_nodes_b, memory_b, rpa_nodes_s, memory_s, molpro_path, molpro_key = ini.get_rpa()

    # generate Input file and scr file
    bilayer_path = os.path.join(path, 'rpa')
    upper_path = os.path.join(bilayer_path, 'upperlayer')
    under_path = os.path.join(bilayer_path, 'underlayer')
    bilayer_job = Job(bilayer_path)
    upper_job = Job(upper_path)
    under_job = Job(under_path)
    rpa_jobs_finished, rpa_jobs_new = [], []
    if not RPA.if_cal_finish(bilayer_job):
        Inp = RPA.RPAInput(bilayer_job, memory_b)
        Inp.generate_input()
        Scr = RPA.Scr(bilayer_job, rpa_nodes_b, molpro_key, molpro_path)
        Scr.gen_scr()
        rpa_jobs_new.append(bilayer_job)
    else:
        bilayer_job.status = 'finished'
        rpa_jobs_finished.append(bilayer_job)
    for job in [upper_job, under_job]:
        if not RPA.if_cal_finish(job):
            Inp = RPA.RPAInput(job, memory_s)
            Inp.generate_input()
            Scr = RPA.Scr(job, rpa_nodes_s, molpro_key, molpro_path)
            Scr.gen_scr()
            rpa_jobs_new.append(job)
        else:
            job.status = 'finished'
            rpa_jobs_finished.append(job)

    # submit jobs
    if len(rpa_jobs_new) > 0:
        new_finished_jobs = RPA.submit(rpa_jobs_new)
        rpa_jobs_finished += new_finished_jobs
    # read and record results
    read_record_results(path, rpa_jobs_finished, RPA.get_energy, method='rpa')

    rec = 'LRPA finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)

