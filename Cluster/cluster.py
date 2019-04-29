#!/usr/bin/python3
import os
import Cluster
from Components import IniReader
from Components import Job
from Components import record_data_json
from OsComponents import record


def cluster(path):

    rec = 'Cluster Cutting begins.\n'
    rec += '---'*25
    print(rec)
    record(path, rec)

    # read infos from input.ini file
    Ini = IniReader()
    project_name, system_type, group_type, lattice_parameter, number_atoms, geometry, fixed_atoms = Ini.get_basic_info()
    central_atoms, factors, deleted_atoms, coord, add_h, out_layer_number = Ini.get_cluster()
    cutting_setting = [coord, add_h]
    record_data_json(path, 'central atoms', central_atoms, section='cluster')
    record_data_json(path, 'cutting factors', factors, section='cluster')
    record_data_json(path, 'deleted atoms', deleted_atoms, section='cluster')
    cutting_setting_dict = {'coord': coord, 'add_h': add_h, 'out_layer_number': out_layer_number}
    record_data_json(path, 'cutting setting', cutting_setting_dict, section='cluster')

    geo_file = os.path.join(os.path.join(path, 'geo_opt'), 'geo_opt.out')
    job = os.path.join(path, 'cluster')
    job = Job(job)

    Clu = Cluster.ClusterCutter(
        job,
        geo_file,
        factors=factors,
        name=project_name,
        central_atoms=central_atoms,
        fixed_atoms=fixed_atoms,
        cutting_setting=cutting_setting,
        deleted_atoms=deleted_atoms
    )
    Clu.get_cluster()

    if out_layer_number is True:
        Clu.write_xyz_with_layernumber()
    else:
        Clu.write_xyz()

    rec = 'Cluster Cutting finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)
