#!/usr/bin/python3
import os
import json
from copy import deepcopy
from Components import unit_transform
from Components import is_number


class Result(object):

    def __init__(self, job='', energy=0, unit='hartree'):
        self.job = job
        self.path = job.path
        self.method = job.method
        self.step = self.get_step()
        self.bs = self.get_bs_type()
        self.energy, self.unit = energy, unit
        assert is_number(self.energy)
        self.energy = float(self.energy)

    def __repr__(self):
        return '{}: {} {}'.format(self.method, self.energy, self.unit)

    def __sub__(self, other):
        assert type(other) == Result
        if other.unit != self.unit:
            other.energy = unit_transform(other.energy, other.unit, self.unit)
            other.unit = self.unit
        new_Res = deepcopy(self)
        new_Res.energy = self.energy - other.energy
        return new_Res

    def __add__(self, other):
        assert type(other) == Result
        if other.unit != self.unit:
            other.energy = unit_transform(other.energy, other.unit, self.unit)
            other.unit = self.unit
        new_Res = deepcopy(self)
        new_Res.energy = self.energy + other.energy
        return new_Res

    def __mul__(self, scalar):
        return Result(self.job, self.energy*scalar, self.unit)

    def __truediv__(self, scalar):
        return Result(self.job, self.energy/scalar, self.unit)

    def __pow__(self, power, modulo=None):
        return Result(self.job, self.energy**power, self.unit)

    def get_step(self):
        step = self.method.split('_')
        step = step[1:]
        step = '_'.join(step)
        return step

    def get_bs_type(self):
        bs = self.method.split('_')[0]
        return bs

    def record_data_json(self, items):
        path = self.job.root_path
        json_file = os.path.join(path, 'results.json')
        with open(json_file, 'r') as f:
            data = json.load(f)
        if 'results' not in data:
            data['results'] = {}
        results_data = data['results']
        for i in range(len(items)):
            if i == 0:
                if items[0] not in results_data:
                    results_data[items[0]] = {}
                item_dict = results_data[items[0]]
            elif i == len(items) - 1:
                item_dict[items[i]] = [self.energy, self.unit]
            else:
                if items[i] not in item_dict:
                    item_dict[items[i]] = {}
                item_dict = item_dict[items[i]]
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=4)

