#!/usr/bin/python3
import os
from Components import IniReader
from Components import record_data_json
from Components import Job
from OsComponents import record
import Loc


def localization(path):

    rec = 'Localization begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    ini = IniReader()
    nodes, crystal_path = ini.get_loc()
    record_data_json(path, 'nodes', nodes, section='loc')

    # generate jobs
    bilayer_path = os.path.join(path, 'loc')
    upper_path = os.path.join(bilayer_path, 'upperlayer')
    under_path = os.path.join(bilayer_path, 'underlayer')
    bilayer_job = Job(bilayer_path)
    upper_job = Job(upper_path)
    under_job = Job(under_path)
    loc_jobs = [bilayer_job, upper_job, under_job]
    loc_jobs_finished, loc_jobs_new = [], []
    # check job and copy input file
    for job in loc_jobs:
        if not Loc.if_loc_finish(job):
            loc_jobs_new.append(job)
            Loc.copy_inp_file(job)
            Loc.copy_loc_scr(job, nodes, crystal_path)
        else:
            job.status = 'finished'
            loc_jobs_finished.append(job)

    # submit jobs
    if len(loc_jobs_new) > 0:
        new_finished_jobs = Loc.submit(loc_jobs_new)
        loc_jobs_finished += new_finished_jobs

    rec = 'Localization finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)
