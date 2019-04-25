#!/usr/bin/python3
import os
import re


def if_loc_finish(job):
    path = job.path
    """
    check the localization is finished or not through the output file
    :param path: string
    :return: Bool True of False
    """
    out_file = os.path.join(path, 'loc.out')
    if not os.path.exists(out_file):
        return False
    else:
        with open(out_file, 'r') as f:
            lines = f.read().replace('\n', ':')
        lines = ' '.join(lines.split()) + '#'
        regex = 'TERMINATION.*#'
        line = re.search(regex, lines)
        if line is None:
            return False
        else:
            return True
