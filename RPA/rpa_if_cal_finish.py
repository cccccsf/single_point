#!/usr/bin/python3
import os


def if_cal_finish(job):
    path = job.path
    out_path = os.path.join(path, 'rpa.out')
    if not os.path.exists(out_path):
        return False
    else:
        with open(out_path, 'rb') as f:
            f.seek(-300, 2)
            out = f.read().decode('utf-8')
        out = out.split('\n')
        if out[-1] == '':
            last = out[-2]
        else:
            last = out[-1]
        if last == ' Molpro calculation terminated':
            return True
        else:
            return False
