#!/usr/bin/python3
import os
import sys
import shutil
import configparser

class IniReader(object):
    
    def __init__(self, path=''):
        self.ini_path = path
        self.ini_path = elf.set_defalut_ini_path()
        self.cfg = configparser.ConfigParser()
        self.read_ini_file()

        self.project_path, self.start, self.end = self.read_ini_info()


        
    def set_defalut_ini_path(self):
        if self.ini_path != '':
            return self.ini_path
        else:
            self.ini_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
            self.ini_path = os.path.join(self.ini_path, 'input.ini')
            return self.ini_path

    def read_ini_file(self):
        try:
            self.cfg.read(self.ini_path, encoding='utf-8')
        except Exception as e:
            print(e)

    def read_ini_info(self):
        try:
            path = self.cfg.get('Initilization', 'path')
            start = self.cfg.get('Initilization', 'start')
            end = self.cfg.get('Initilization', 'end')
        except configparser.NoOptionError:
            print(configparser.NoOptionError)
            sys.exit()
        return path, start, end

    def read

