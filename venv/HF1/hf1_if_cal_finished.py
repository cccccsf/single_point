#!/usr/bin/python3
import os
import re

def if_cal_finish(job):
    """
    check the calculation is finished or not through the output file
    :param path: string
    :return: Bool Ture of False
    """
    path = job.path
    out_file = os.path.join(path, 'hf.out')
    try:
        if not os.path.exists(out_file):
            return False
        else:
            with open(out_file, 'r') as f:
                lines = f.read().replace('\n', ':')
            lines = ' '.join(lines.split()) + '#'
            regex = 'TOTAL CPU TIME'
            line = re.search(regex, lines)
            if line == None:
                return False
            else:
                if line.group(0) != 'TOTAL CPU TIME':
                    return False
                else:
                    return True
        return True
    except FileNotFoundError as e:
        return False
