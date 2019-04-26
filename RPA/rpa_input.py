#!/usr/bin/python3
import os
import re
import shutil
from OsComponents import mkdir


class RPAInput(object):

    def __init__(self, job, memory='12000'):
        self.rpa_job = job
        self.rpa_path = job.path
        self.memory = memory
        self.inp_file = os.path.join(self.rpa_path, 'rpa.inp')

    def copy_molpro_inp(self):
        mkdir(self.rpa_path)
        inp_from = self.rpa_path.replace('rpa', 'lmp2')
        inp_from = os.path.join(inp_from, 'molpro.inp')
        shutil.copy(inp_from, self.inp_file)

    def change_form_molpro_inp(self):
        # only for shell, not windows
        # os.chdir(path)
        # com_memory = 'sed -i -e \'s/1536/{}/g\' rpa.inp'.format(memory)
        # subprocess.call(com_memory, shell=True)
        with open(self.inp_file, 'r') as f:
            molpro_inp = f.read()
        memory_formal = '1536'
        try:
            line0 = re.search('memory.*?\n', molpro_inp).group(0)
            line0 = line0.split(',')
            memory_formal = line0[1]
        except Exception as e:
            print(e)
            print('Fail to read formal memory size')
        molpro_inp = re.sub('{}'.format(memory_formal), '{}'.format(self.memory), molpro_inp, count=1)
        molpro_inp = re.sub('P\s+', 'p', molpro_inp)
        with open(self.inp_file, 'w') as f:
            f.write(molpro_inp)

    def generate_input(self):
        self.copy_molpro_inp()
        self.change_form_molpro_inp()
