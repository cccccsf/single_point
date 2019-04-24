#!/usr/bin/python3
import os
from OsComponents import record
from Components import IniReader
from Components import Job
from Components import record_data_json
from Crystal import Geometry
import GeoOpt



def geo_opt(path):

    rec = 'Geometry Optimization begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    Ini = IniReader()
    project_name, system_type, group_type, lattice_parameter, number_atoms, geometry, fixed_atoms = Ini.get_basic_info()
    record_data_json(path, 'project_name', project_name)
    record_data_json(path, 'system_type', system_type)
    record_data_json(path, 'lattice_parameter', lattice_parameter)
    record_data_json(path, 'geometry', geometry)
    record_data_json(path, 'fixed_atoms', fixed_atoms)
    if isinstance(fixed_atoms, list) and len(fixed_atoms) == 2:
        geometry = Geometry(geometry=geometry, fixed_atoms=fixed_atoms)
    else:
        geometry = Geometry(geometry=geometry)
    bs, functional, nodes, crystal_path = Ini.get_geo_opt()
    record_data_json(path, 'basis_set', bs, section='geo_opt')
    record_data_json(path, 'functional', functional, section='geo_opt')
    record_data_json(path, 'nodes', nodes, section='geo_opt')

    job = os.path.join(path, 'geo_opt')
    job = Job(job)
    if not GeoOpt.if_job_finish(job):
        # generation of INPUT
        Geo_Inp = GeoOpt.Geo_Opt_Input(
            job,
            project_name,
            system_type,
            group_type,
            lattice_parameter,
            geometry,
            bs,
            functional)
        Geo_Inp.gen_input()
        # copy file and submit the job
        job = GeoOpt.submit(job, nodes, crystal_path, path)
    else:
        job.status = 'finished'

    # read and record the results
    GeoOpt.read_record_result(job, path)

    rec = 'Geometry optimization finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)

