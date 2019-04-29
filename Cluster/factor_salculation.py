#!/usr/bin/python3
import math
from Components import Atom
from Cluster import ClusterCutter


class FactorCalculator(ClusterCutter):

    def __init__(
            self,
            atom,
            path,
            geometry_file,
            factors=[1, 1, 0.7],
            name='cluster',
            central_atoms=[],
            fixed_atoms=[],
            deleted_atoms=[],
            cutting_setting=[]
                ):
        super(FactorCalculator, self).__init__(
            path,
            geometry_file,
            factors,
            name,
            central_atoms,
            fixed_atoms,
            deleted_atoms,
            cutting_setting
            )
        self.atom = atom
        self.layer = self.locate_atom()
        self.center = self.get_center()

    def get_distance_to_center(self, atom=[], fraction=False):

        if type(self.atom) == Atom:
            x, y, z = self.atom.x, self.atom.y, self.atom.z
        elif len(atom) == 3:
            x, y, z = atom

        if self.dimensionality == 2:
            x0, y0 = self.center
            dis = math.sqrt((x-x0)**2 + (y-y0)**2)
            print('distance: ', dis)
        else:
            x0, y0, z0 = self.center
            dis = math.sqrt((x-x0)**2 + (y-y0)**2 + (z-z0)**2)
            print('The distance between the given atom and the central point is: ', dis)

        if fraction is True:
            return round(dis/self.l, 2)
        else:
            return dis

    def get_distance_to_vector(self, vec, fraction=False):

        if type(vec) == tuple and len(vec) == 3:
            vx, vy, vz = vec
            l = math.sqrt(vx**2 + vy**2 + vz**2)
        elif vec in ['a', 'b', 'c'] or int(vec) in [1, 2, 3] or vec in ['x', 'y' 'z']:
            if vec == 'a' or vec == 'x' or int(vec) == 1:
                vector = self.lattice_vector[0]
                l = self.l1
            elif vec == 'b' or vec == 'y' or int(vec) == 2:
                vector = self.lattice_vector[1]
                l = self.l2
            elif vec == 'c' or vec == 'z' or int(vec) == 3:
                vector = self.lattice_vector[2]
                l = self.l3
        vx, vy, vz = vector

        if type(self.atom) == Atom:
            x, y, z = self.atom.x, self.atom.y, self.atom.z
        else:
            x, y, z = self.atom

        if self.dimensionality == 2:
            cx, cy = self.center
            ux = x - cx
            uy = y - cy
            proj = (ux*vx + uy*vy) / math.sqrt(vx**2 + vy**2)
            print('projection : ', proj)
        else:
            cx, cy, cz = self.center
            ux = x - cx
            uy = y - cy
            uz = z - cz
            proj = (ux*vx + uy*vy + uz*vz) / math.sqrt(vx**2 + vy**2 + vz**2)
            print('projection : ', proj)

        if fraction is True:
            return abs(round(proj/l, 2))
        else:
            return abs(proj)

    def locate_atom(self):
        """
        judging whether the atom is in unpperlayer or in underlayer
        :return: layer ( 1 for upperlaye and 0 for underlayer )
        """
        if float(self.atom.z) >= max(self.z_fixed) - 0.15:
            layer = 1
        else:
            layer = 0
        self.atom.layer = layer
        return layer

    def get_center(self):
        if self.layer == 1:
            center = self.UnderCenter
        elif self.layer == 0:
            center = self.UpperCenter
        else:
            center = self.centre
        return center
