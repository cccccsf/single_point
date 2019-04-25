#!/usr/bin/python3
import os
import sys
from Crystal import Guesdual
from Crystal import Basis_set
from Crystal import Geometry
from Crystal import choose_shrink
from OsComponents import mkdir
from Components import read_from_record


class Input(object):

    def __init__(self, job, name, slab_or_molecule, layer_group, bs_type='default', fixed_atoms = []):
        self.hf2_job = job
        self.job_path = self.hf2_job.path
        self.root_path = job.root_path
        self.input_path = os.path.join(self.job_path, 'INPUT')

        self.name = name
        self.slab_or_molecule = slab_or_molecule
        self.layer_group = layer_group
        self.fixed_atoms = fixed_atoms

        self.geometry = self.get_geometry()         # class Crystal.Geometry
        self.lattice_parameter = self.get_lattice_parameter()

        self.bs = []                # class Crystal.Basis_set
        self.bs_type = bs_type

    def get_geometry(self):
        try:
            geometry = read_from_record(
                self.root_path, 'optimized_geometry', 'geo_opt')
            if isinstance(
                    self.fixed_atoms, list) and len(
                    self.fixed_atoms) == 2:
                geometry = Geometry(
                    geometry=geometry,
                    fixed_atoms=self.fixed_atoms)
            else:
                geometry = Geometry(geometry=geometry)
        except KeyError as e:
            print(e)
            print('Optimized lattice parameter not found!'
                  'Please check out?')
            sys.exit()  # here need a better way to deal with
        return geometry

    def get_lattice_parameter(self):
        try:
            latt_para = read_from_record(
                self.root_path, 'optimized_lattice_parameter', 'geo_opt')
            latt_para = [float(i) for i in latt_para]
            if self.slab_or_molecule == 'SLAB' and len(latt_para) == 6:
                latt_para = latt_para[:2] + latt_para[-1:]
                l = latt_para[:2]
                a = latt_para[-1:]
                new_latt_patt = [l, a]
            elif len(latt_para) == 6:
                l = latt_para[:3]
                a = latt_para[3:]
                new_latt_patt = [l, a]
            else:
                l = [i for i in latt_para if i <= 20]
                a = [i for i in latt_para if i > 20]
                new_latt_patt = [l, a]
            return new_latt_patt
        except KeyError as e:
            print(e)
            print('Optimized lattice parameter not found!'
                  'Please check out?')
            return []

    def write_basis_info(self):
        mkdir(self.job_path)
        with open(self.input_path, 'w') as f:
            f.write(self.name + '\n')
            f.write(self.slab_or_molecule + '\n')
            f.write(str(self.layer_group) + '\n')

    def write_lattice_parameter(self):
        with open(self.input_path, 'a') as f:
            for l in self.lattice_parameter[0]:
                f.write(str(l) + ' ')
            for a in self.lattice_parameter[1]:
                f.write(str(a) + ' ')
            f.write('\n')

    def write_geometry(self):
        self.geometry.write_geometry(self.input_path)
        with open(self.input_path, 'a') as f:
            f.write('END' + '\n')

    def write_bs(self):
        if len(self.bs) == 0:
            self.generate_bs()
        self.bs.write_bs(self.input_path)
        with open(self.input_path, 'a') as f:
            f.write('99' + ' ' + '0' + '\n')
            f.write('END' + '\n')

    def generate_bs(self):
        self.bs = Basis_set(self.geometry.elements, 'HF2', self.bs_type)

    def guesdual(self):
        guesdual = Guesdual(self.bs)
        guesdual.write_guesdual(self.input_path)

    def write_cal_info(self):
        shrink = choose_shrink(self.lattice_parameter)
        shrink = str(shrink)
        with open(self.input_path, 'a') as f:
            f.write('SHRINK' + '\n')
            f.write(shrink + ' ' + shrink + '\n')
            f.write('TOLINTEG' + '\n')
            f.write('10' + ' ' + '10' + ' ' + '10' + ' ' + '25' + ' ' + '75' + '\n')
            f.write('SETINF' + '\n')
            f.write('2' + '\n')
            f.write('41' + ' ' + '30' + '\n')
            f.write('43' + ' ' + '20' + '\n')
            f.write('MAXCYCLE' + '\n')
            f.write('60' + '\n')
            f.write('FMIXING' + '\n')
            f.write('60' + '\n')
            f.write('ANDERSON' + '\n')
            f.write('EXCHSIZE' + '\n')
            f.write('30000000' + '\n')
            f.write('BIPOSIZE' + '\n')
            f.write('30000000' + '\n')

    def write_end(self):
        with open(self.input_path, 'a') as f:
            f.write('END' + '\n')
            f.write('END' + '\n')

    def gen_input(self):
        self.write_basis_info()
        self.write_lattice_parameter()
        self.write_geometry()
        self.write_bs()
        self.write_cal_info()
        self.guesdual()
        self.write_end()
