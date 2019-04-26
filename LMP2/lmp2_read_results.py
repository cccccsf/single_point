#!/usr/bin/python3
import os
import re
from Components import read_record_results


def get_energy_lmp2(job):

    path = job.path
    path = os.path.join(path, 'lmp2.out')
    with open(path, 'r') as f:
        lines = f.read()
        regex = 'FINAL SUMMARY.*?\*+.*?\*\*+'
    final_summary = re.search(regex, lines, re.M|re.S)
    if final_summary is not None:
        final_summary = final_summary.group(0)
    else:
        print(path)
        print('Energy information not found...')

    regex = 'MP2 CORRELATION ENERGY.*?\n'
    lmp2 = re.search(regex, final_summary)
    if lmp2 is not None:
        lmp2 = lmp2.group(0)
        lmp2 = lmp2.strip()
        lmp2 = lmp2.split()
        lmp2 = lmp2[-2]
    else:
        print(path)
        print('LMP2 erengy not found...')
    unit = 'hartree'    # here need more

    return lmp2, unit


"""
                                FINAL SUMMARY

 *******************************************************************************
 *                                                                             *
 *                                          HF ENERGY:   0.0000000000E+00      *
 *                                     SINGLES ENERGY:   0.0000000000E+00      *
 *                             MP2 CORRELATION ENERGY:  -0.6353830194E+00      *
 *                              HF+SINGLES+MP2 ENERGY:  -0.6353830194E+00      *
 *                        HF+SINGLES+E(GRIMME) ENERGY:  -0.6041517836E+00      *
 *                                                                             *
 *******************************************************************************
 """


def get_energy_scs(job):

    path = job.path
    path = os.path.join(path, 'lmp2.out')
    with open(path, 'r') as f:
        lines = f.read()
        regex = 'FINAL SUMMARY.*?\*+.*?\*\*+'
    final_summary = re.search(regex, lines, re.M|re.S)
    if final_summary is not None:
        final_summary = final_summary.group(0)
    else:
        print(path)
        print('Energy infomation not found...')

    regex = 'HF\+SINGLES\+E\(GRIMME\).*?\n'
    scs = re.search(regex, final_summary)
    if scs is not None:
        scs = scs.group(0)
        scs = scs.strip()
        scs = scs.split()
        scs = scs[-2]
    unit = 'hartree'    # here need more

    return scs, unit


def lmp2_read_record_results(path, jobs):
    read_record_results(path, jobs, get_energy_lmp2, method='lmp2')
    read_record_results(path, jobs, get_energy_scs, method='scs_lmp2')
