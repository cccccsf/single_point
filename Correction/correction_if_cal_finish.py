#!/usr/bin/python3
import os
import re


def if_cal_finish(job):
    path = job.path
    out_file = os.path.join(path, job.method) + '.out'
    if not os.path.exists(out_file):
        return False
    else:
        with open(out_file, 'rb') as f:
            f.seek(-2000, 2)
            lines = f.read().decode('utf-8')
        pattern = 'Molpro calculation terminated'
        termi = re.search(pattern, lines)
        if termi is None:
            return False
        else:
            if termi.group(0) != 'Molpro calculation terminated':
                return False
            return True
