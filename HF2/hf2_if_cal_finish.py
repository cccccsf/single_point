#!/usr/bin/python3
import os
import re


def if_cal_finish(job):
    """
    check the calculation is finished or not through the output file
    :param job: Components.Job
    :return: Bool True of False
    """
    path = job.path
    if not os.path.exists(path):
        return False
    os.chdir(path)
    if not os.path.exists('hf.out'):
        return False
    else:
        file = open('hf.out', 'r')
        lines = file.read().replace('\n', ':')
        file.close()
        lines = ' '.join(lines.split()) + '#'
        regex = 'TOTAL CPU TIME'
        line = re.search(regex, lines)
        if line is None:
            return False
        else:
            if line.group(0) != 'TOTAL CPU TIME':
                return False
            else:
                return True
