#!/usr/bin/python3


def get_extrapolated_correction(e1, e2, x, y):
    """
    get the extrapolated basis-set limit Exy
    :param e1: energy with basis-set of cardinal number x
    :param e2: energy with basis-set of cardinal number y
    :param x: the cardinal number of the first basis-set
    :param y: the cardinal number of the second basis-set
    :return:
    """
    # a = e1 * x**3
    # print(a)
    # import sys
    # sys.exit()
    return (e1 * x**3 - e2 * y**3) / (x**3 - y**3)
