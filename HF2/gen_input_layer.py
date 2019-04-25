#!/usr/bin/python3
import re
from HF2 import Input
from Crystal import Basis_set


class LayerInp(Input):

    def __init__(
            self,
            hf1_job,
            name,
            slab_or_molecule,
            layer_group,
            bs_type='default',
            layertype='upperlayer',
            fixed_atoms=[]):
        super(
            LayerInp,
            self).__init__(
            hf1_job,
            name,
            slab_or_molecule,
            layer_group,
            bs_type,
            fixed_atoms=fixed_atoms)
        self.layertype = layertype
        self.ghost = self.read_ghost()

    def read_ghost(self):
        hf1_path = self.job_path.replace('hf2', 'hf1')
        file = hf1_path + '/INPUT'
        with open(file) as f:
            lines = f.read().replace('\n', ':')
        lines = ' '.join(lines.split())

        regex = 'GHOSTS.*?END'
        ghost = re.search(regex, lines).group(0)
        ghost = re.split(':', ghost.replace(': ', ':'))
        return ghost

    def write_bs(self):
        self.bs = Basis_set(self.geometry.elements, 'HF2', self.bs_type)
        self.bs.write_bs(self.input_path)
        with open(self.input_path, 'a') as f:
            f.write('99' + ' ' + '0' + '\n')
            for unit in self.ghost:
                f.write(str(unit) + '\n')
            f.write('END' + '\n')
