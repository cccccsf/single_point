#!/usr/bin/python3
import os
from Components import IniReader
from Components import record_data_json
from Components import Job
from OsComponents import record
import HF2


def hf2(path):

    rec = 'Second Hartree Fock Calculation begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    Ini = IniReader()
    project_name, system_type, group_type, lattice_parameter, number_atoms, geometry, fixed_atoms = Ini.get_basic_info()
    bs, nodes, crystal_path = Ini.get_hf2()
    record_data_json(path, 'basis_set', bs, section='hf2')
    record_data_json(path, 'nodes', nodes, section='hf2')

    # generation of INPUT
    bilayer_path = os.path.join(path, 'hf2')
    upper_path = os.path.join(bilayer_path, 'upperlayer')
    under_path = os.path.join(bilayer_path, 'underlayer')
    bilayer_job = Job(bilayer_path)
    upper_job = Job(upper_path)
    under_job = Job(under_path)
    hf2_jobs_finished, hf2_jobs_new = [], []
    if not HF2.if_cal_finish(bilayer_job):
        inp = HF2.Input(
            bilayer_job,
            project_name,
            system_type,
            group_type,
            bs_type=bs,
            fixed_atoms=fixed_atoms
        )
        inp.gen_input()
        HF2.copy_submit_scr(bilayer_job, nodes, crystal_path)
        hf2_jobs_new.append(bilayer_job)
    else:
        bilayer_job.status = 'finished'
        hf2_jobs_finished.append(bilayer_job)
    if not HF2.if_cal_finish(upper_job):
        inp = HF2.LayerInp(
            upper_job,
            project_name,
            system_type,
            group_type,
            bs_type=bs,
            layertype='upperlayer',
            fixed_atoms=fixed_atoms
        )
        inp.gen_input()
        HF2.copy_submit_scr(upper_job, nodes, crystal_path)
        hf2_jobs_new.append(upper_job)
    else:
        upper_job.status = 'finished'
        hf2_jobs_finished.append(upper_job)
    if not HF2.if_cal_finish(under_job):
        inp = HF2.LayerInp(
            under_job,
            project_name,
            system_type,
            group_type,
            bs_type=bs,
            layertype='underlayer',
            fixed_atoms=fixed_atoms
        )
        inp.gen_input()
        HF2.copy_submit_scr(under_job, nodes, crystal_path)
        hf2_jobs_new.append(under_job)
    else:
        under_job.status = 'finished'
        hf2_jobs_finished.append(under_job)

    # copy files and submit jobs
    if len(hf2_jobs_new) > 0:
        new_finished_jobs = HF2.submit(hf2_jobs_new)
        hf2_jobs_finished += new_finished_jobs

    # read and record results
    HF2.read_record_results(path, hf2_jobs_finished)

    rec = 'HF2 finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)


