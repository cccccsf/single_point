#!/usr/bin/python3
import os
import Components
import Cluster


def cluster_cutting(atom):

    Ini = Components.IniReader()
    path = Ini.project_path
    project_name, system_type, group_type, lattice_parameter, number_atoms, geometry, fixed_atoms = Ini.get_basic_info()
    central_atoms, factors, deleted_atoms, coord, add_h, out_layer_number = Ini.get_cluster()
    cutting_setting = [coord, add_h]
    geo_file = os.path.join(os.path.join(path, 'geo_opt'), 'geo_opt.out')
    cluster_path = os.path.join(path, 'cluster')

    FacCal = Cluster.FactorCalculator(
        atom,
        cluster_path,
        geo_file,
        factors=factors,
        name=project_name,
        central_atoms=central_atoms,
        fixed_atoms=fixed_atoms,
        cutting_setting=cutting_setting,
        )
    # FacCal.get_cluster()

    print('***'*30)
    print(atom)
    dimen = FacCal.dimensionality
    if dimen == 2:
        print('central axis: {}'.format(FacCal.center))
    else:
        print('central point: {}'.format(FacCal.center))
    print('---'*30)
    dis_fac = FacCal.get_distance_to_center(fraction=True)
    print('factor of distance: ', dis_fac)
    print('---'*30)
    a_fac = FacCal.get_distance_to_vector(vec=1, fraction=True)
    print('factor of lattice vector 1: ', a_fac)
    print('---'*30)
    b_fac = FacCal.get_distance_to_vector(vec=2, fraction=True)
    print('factor of lattice vector 2: ', b_fac)
    if dimen != 2:
        c_fac = FacCal.get_distance_to_vector(vec=3, fraction=True)
        print('---'*30)
        print('factor of lattice vector 3: ', c_fac)
    print('***'*30)


if __name__ == "__main__":

    # please write down the atom information here
    element = 15
    x = 0
    y = 0
    z = 0

    atom = Components.Atom(element, x, y, z)
    cluster_cutting(atom)
