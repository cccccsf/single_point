#!/usr/bin/python3
import os
import re


def if_cal_finish(job):
    path = job.path
    out_path = os.path.join(path, 'lmp2.out')
    if not os.path.exists(out_path):
        return False
    else:
        with open(out_path, 'rb') as f:
            f.seek(-1000, 2)
            out = f.read().decode('utf-8')
        regex = 'TERMINATION  DATE'
        termination = re.search(regex, out)
        if termination is None:
            return False
        else:
            if termination.group(0) != 'TERMINATION  DATE':
                return False
            else:
                return True
