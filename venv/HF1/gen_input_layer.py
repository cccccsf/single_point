#!/usr/bin/python3
from HF1 import Input

class Layer_Inp(Input):

    def __init__(self, job, name, slab_or_molecule, layer_group, bs_type, fiexed_atoms = [], layertype='upperlayer'):
        super(Layer_Inp, self).__init__(job, name, slab_or_molecule, layer_group, bs_type, fiexed_atoms=fiexed_atoms)
        self.layertype = layertype
        self.ghost_info = self.get_ghost()



    def get_ghost(self):
        count = 1
        geo_z = [float(i) for i in self.geometry.z]
        fixed_z = [float(i) for i in self.geometry.z_fixed_co]
        th = (self.geometry.layer_distance)/7
        under, upper = [], []
        for z in geo_z:
            if z <= min(fixed_z) or abs(z - min(fixed_z)) <= th:
                under.append(count)
            else:
                upper.append(count)
            count += 1
        if self.layertype == 'underlayer':
            return upper
        else:
            return under


    def write_ghost(self):
        with open(self.input_path, 'a') as f:
            f.write('GHOSTS' + '\n')
            f.write(str(len(self.ghost_info)) + '\n')
            for atom in self.ghost_info:
                f.write(str(atom) + ' ')
            f.write('\n')


    def write_bs(self):
        self.bs.write_bs(self.input_path)
        with open(self.input_path, 'a') as f:
            f.write('99' + ' ' + '0' + '\n')
        self.write_ghost()
        with open(self.input_path, 'a') as f:
            f.write('END' + '\n')
