#!/usr/bin/python3
from Data import periodic_table_rev


class Atom(object):

    def __init__(self, nat, x, y, z, no=1, atom_type=1, coor=1, coor_vec=[]):
        self.nat = nat
        self.element = periodic_table_rev[int(nat)]
        self.x = x
        self.y = y
        self.z = z
        self.no = no
        self.type = atom_type
        self.coor = coor
        self.coor_vec = coor_vec
        self.coor_vec_free = []
        self.layer = 1  # here 1 for upperlayer and 0 for underlayer

    def __repr__(self):
        return str(self.nat).ljust(5) + ' ' + '{:.12E}'.format(float(self.x)).rjust(19) + ' ' + '{:.12E}'.format(float(self.y)).rjust(19) + ' ' + '{:.12E}'.format(float(self.z)).rjust(19)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __setitem__(self, key, value):
        self.__dict__[key] = value
