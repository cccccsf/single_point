#!/usr/bin/python3
import os
import sys
import json


def read_from_record(path, item, section='basis'):
    json_file = os.path.join(path, 'results.json')
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(e)
        print('Record file not found.')
        print('Please check and try again.')
        sys.exit()
    try:
        value = data[section][item]
    except KeyError as e:
        print(e)
        print('Please write the correct key and try again.')
        sys.exit()
    return value
