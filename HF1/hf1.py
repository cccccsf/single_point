#!/usr/bin/python3
import os
from Components import IniReader
from Components import read_from_record
from Components import record_data_json
from Components import Job
from OsComponents import record
from Crystal import Geometry
import HF1


def hf1(path):

    rec = 'First Hartree Fock Calculation begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    Ini = IniReader()
    project_name, system_type, group_type, lattice_parameter, number_atoms, geometry, fixed_atoms = Ini.get_basic_info()
    geometry = read_from_record(path, 'optimized_geometry', 'geo_opt')
    if isinstance(fixed_atoms, list) and len(fixed_atoms) == 2:
        geometry = Geometry(geometry=geometry, fixed_atoms=fixed_atoms)
    else:
        geometry = Geometry(geometry=geometry)
    lattice_parameter = read_from_record(path, 'optimized_lattice_parameter', 'geo_opt')
    bs, nodes, crystal_path = Ini.get_hf1()
    record_data_json(path, 'basis_set', bs, section='hf1')
    record_data_json(path, 'nodes', nodes, section='hf1')

    # generation of INPUT
    bilayer_path = os.path.join(path, 'hf1')
    job = Job(bilayer_path)
    hf1_jobs = []
    hf1_jobs_finished = []
    if not HF1.if_cal_finish(job):
        Inp = HF1.Input(
            job,
            project_name,
            system_type,
            group_type,
            bs,
            fiexed_atoms=fixed_atoms
        )
        Inp.gen_input()
        hf1_jobs.append(job)
        HF1.copy_submit_scr(job, nodes, crystal_path)
    else:
        job.status = 'finished'
        hf1_jobs_finished.append(job)
    upper_path = os.path.join(bilayer_path, 'upperlayer')
    upper_job = Job(upper_path)
    if not HF1.if_cal_finish(upper_job):
        Inp = HF1.Layer_Inp(
            upper_job,
            project_name,
            system_type,
            group_type,
            bs,
            fiexed_atoms=fixed_atoms,
            layertype='upperlayer'
        )
        Inp.gen_input()
        hf1_jobs.append(upper_job)
        HF1.copy_submit_scr(upper_job, nodes, crystal_path)
    else:
        upper_job.status = 'finished'
        hf1_jobs_finished.append(upper_job)
    under_path = os.path.join(bilayer_path, 'underlayer')
    under_job = Job(under_path)
    if not HF1.if_cal_finish(under_job):
        Inp = HF1.Layer_Inp(
            under_job,
            project_name,
            system_type,
            group_type,
            bs,
            fiexed_atoms=fixed_atoms,
            layertype='underlayer'
        )
        Inp.gen_input()
        hf1_jobs.append(under_job)
        HF1.copy_submit_scr(upper_job, nodes, crystal_path)
    else:
        under_job.status = 'finished'
        hf1_jobs_finished.append(under_job)

    # copy files and submit jobs
    new_finished_jobs = HF1.submit(hf1_jobs)
    hf1_jobs_finished += new_finished_jobs

    # read and record the results
    HF1.read_record_results(path, hf1_jobs_finished)

    rec = 'HF1 finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)

