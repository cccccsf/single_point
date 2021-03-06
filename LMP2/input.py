#!/usr/bin/python3
import os
import re
import sys
from OsComponents import mkdir


class Lmp2Input(object):

    def __init__(self, job):
        self.job = job
        self.lmp2_path = job.path
        self.input_path = os.path.join(self.lmp2_path, 'INPUT')
        self.ghost = []

    def write_part1(self):
        mkdir(self.lmp2_path)
        with open(self.input_path, 'w') as f:
            f.write('READC14' + '\n')
            f.write('DUALBAS' + '\n')
            f.write('KNET' + '\n')
            f.write('8' + '\n')
            f.write('MEMORY' + '\n')
            f.write('40000' + '\n')
            f.write('NOSYM12' + '\n')
            f.write('CLUSCOR' + '\n')
            f.write('LPairlst' + '\n')
            f.write('100000' + '\n')
            f.write('MOG_DIST' + '\n')
            f.write('9 9' + '\n')
            f.write('NOSING' + '\n')
            f.write('NFITCEL' + '\n')
            f.write('-100' + '\n')
            f.write('STREAMIN' + '\n')
            f.write('SMAL3IDX' + '\n')

    def write_molatoms(self):
        with open(self.input_path, 'a') as f:
            f.write('MOLATOMS' + '\n')
            f.write(self.ghost[1] + '\n')
            for i in self.ghost[2]:
                f.write(i + ' ')
            f.write('\n')

    def write_part2(self):
        with open(self.input_path, 'a') as f:
            f.write('ENVPAIR' + '\n')
            f.write('6. 6.' + '\n')
            f.write('MOLPAIR' + '\n')
            f.write('6. 6.' + '\n')
            f.write('MOENPAIR' + '\n')
            f.write('12. 12.' + '\n')
            f.write('PRINTBIL' + '\n')

    def write_bilayer(self):
        with open(self.input_path, 'a') as f:
            f.write('BILAYER' + '\n')
            print(self.ghost)
            f.write(self.ghost[1] + '\n')
            for i in self.ghost[2]:
                f.write(i + ' ')
            f.write('\n')

    def write_part3(self):
        with open(self.input_path, 'a') as f:
            f.write('DOMPUL' + '\n')
            f.write('0.95' + '\n')
            f.write('IEXT' + '\n')
            f.write('1' + '\n')
            f.write('DFITTING' +'\n')
            f.write('DIRECT' + '\n')
            f.write('G-AVTZ' + '\n')
            f.write('ENDDF' +'\n')
            f.write('PRINPLOT' + '\n')
            f.write('2' + '\n')
            f.write('PRINTMEM' + '\n')
            f.write('END' + '\n')

    def read_ghost(self):
        hf2_path = self.lmp2_path.replace('lmp2', 'hf2')
        hf2_inp = os.path.join(hf2_path, 'upperlayer')
        hf2_inp = os.path.join(hf2_inp, 'INPUT')
        with open(hf2_inp) as f:
            inp = f.read()
        regex = 'GHOSTS\n.*?\n.*?\nEND'
        try:
            ghost = re.search(regex, inp).group(0)
        except Exception as e:
            print(e)
            print(self.lmp2_path)
            print('Ghosts infomation can not be found.')
            print('Please exit the programm and check the INPUT file of HF2')
            sys.exit()
        ghost = ghost.split('\n')   #['GHOSTS', '4', '1 2 3 4 ', 'END']
        ghost[2] = ghost[2].strip().split(' ')
        self.ghost = ghost

    def write_input(self):
        self.read_ghost()
        self.write_part1()
        self.write_molatoms()
        self.write_part2()
        self.write_bilayer()
        self.write_part3()


class Lmp2InputLayer(Lmp2Input):

    def __init__(self, job):
        super(Lmp2InputLayer, self).__init__(job)

    def write_part1(self):
        mkdir(self.lmp2_path)
        with open(self.input_path, 'w') as f:
            f.write('READC14' + '\n')
            f.write('DUALBAS' + '\n')
            f.write('KNET' + '\n')
            f.write('8' + '\n')
            f.write('MEMORY' + '\n')
            f.write('40000' + '\n')
            f.write('NOSYM12' +'\n')
            f.write('CLUSCOR' + '\n')
            f.write('LPairlst' + '\n')
            f.write('100000' + '\n')
            f.write('MOG_DIST' + '\n')
            f.write('9 9' + '\n')
            f.write('NOSING' + '\n')
            f.write('NFITCEL' + '\n')
            f.write('-100' + '\n')
            f.write('STREAMIN' + '\n')
            f.write('SMAL3IDX' + '\n')
            f.write('PAIR' + '\n')
            f.write('9. 9.' + '\n')
            f.write('PRINTBIL' + '\n')

    def write_part2(self):
        with open(self.input_path, 'a') as f:
            f.write('DOMPUL' + '\n')
            f.write('0.95' + '\n')
            f.write('IEXT' + '\n')
            f.write('1' + '\n')
            f.write('DFITTING' + '\n')
            f.write('DIRECT' + '\n')
            f.write('G-AVTZ' + '\n')
            f.write('ENDDF' + '\n')
            f.write('PRINPLOT' + '\n')
            f.write('2' + '\n')
            f.write('PRINTMEM' + '\n')
            f.write('END' + '\n')

    def get_ghost(self):
        hf2_path = self.lmp2_path.replace('lmp2', 'hf2')
        hf2_inp = os.path.join(hf2_path, 'INPUT')
        with open(hf2_inp) as f:
            inp = f.read()
        regex = 'GHOSTS\n.*?\n.*?\nEND'
        try:
            ghost = re.search(regex, inp).group(0)
        except Exception as e:
            print(e)
            print(self.lmp2_path)
            print('Ghosts information can not be found.')
            print('Please exit the program and check the INPUT file of HF2')
            sys.exit()
        ghost = ghost.split('\n')   # ['GHOSTS', '4', '1 2 3 4 ', 'END']
        ghost[2] = ghost[2].strip().split(' ')
        self.ghost = ghost

    def write_input(self):
        if len(self.ghost) == 0:
            self.get_ghost()
        self.write_part1()
        self.write_bilayer()
        self.write_part2()
