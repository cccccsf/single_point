#!/usr/bin/python3
import os
import json
from OsComponents import record
from Components import Job
from Components import unit_transform
from Components import IniReader
from Correction import if_cal_finish
from Correction import read_all_results
import Results


def results(path):

    # get jobs
    correction_jobs, root_jobs = get_jobs(path)
    Ini = IniReader()
    unit = Ini.get_unit()

    # read results of correction if not found in 'results.json'
    results_file = os.path.join(path, 'results.json')
    if if_read_record_results_needed(correction_jobs, results_file):
        read_all_results(path, correction_jobs)

    # read formal results
    with open(results_file, 'r') as f:
        data = json.load(f)
    results_dict = {job.method: Results.Result(job, data['correction']['energy'][job.method][0], data['correction']['energy'][job.method][1]) for job in correction_jobs}

    # get extraplation valuess
    extrap_method_error = {}
    extrap_iext1_rpa = {}
    basis_set_correction = {}
    # method error correction
    if 'avdz_rpa_cc' in results_dict and 'avtz_rpa_cc' in results_dict:
        avdtz = Results.get_extrapolated_correction(results_dict['avdz_rpa_cc'], results_dict['avtz_rpa_cc'], 2, 3)
        avdtz.bs = 'avdtz'
        extrap_method_error['avdtz'] = avdtz
    if 'avtz_rpa_cc' in results_dict and 'avqz_rpa_cc' in results_dict:
        avtqz = Results.get_extrapolated_correction(results_dict['avtz_rpa_cc'], results_dict['avqz_rpa_cc'], 3, 4)
        avtqz.bs = 'avtqz'
        extrap_method_error['avtqz'] = avtqz
    for key, value in extrap_method_error.items():
        value.record_data_json(['method error', key])
    # basis set correction
    # iext1
    if 'avdz_iext1_rpa' in results_dict and 'avtz_iext1_rpa' in results_dict:
        avdtz = Results.get_extrapolated_correction(results_dict['avdz_iext1_rpa'], results_dict['avtz_iext1_rpa'], 2, 3)
        avdtz.bs = 'avdtz'
        extrap_iext1_rpa['avdtz'] = avdtz
    if 'avtz_iext1_rpa' in results_dict and 'avqz_iext1_rpa' in results_dict:
        avtqz = Results.get_extrapolated_correction(results_dict['avtz_iext1_rpa'], results_dict['avqz_iext1_rpa'], 3, 4)
        avtqz.bs = 'avtqz'
        extrap_iext1_rpa['avtqz'] = avtqz
    # get basis set correction
    if 'avdtz' in extrap_iext1_rpa:
        avdtz = extrap_iext1_rpa['avdtz'] - results_dict['per_bas_rpa_iext1']
        basis_set_correction['avdtz'] = avdtz
    if 'avtqz' in extrap_iext1_rpa:
        avtqz = extrap_iext1_rpa['avtqz'] - results_dict['per_bas_rpa_iext1']
        basis_set_correction['avtqz'] = avtqz
    for key, value in basis_set_correction.items():
        value.record_data_json(['basis set error', key])

    # HF
    hf_e, hf_unit = read_data_from_json(results_file, ['hf2', 'energy', 'layer_energy'])
    hf_job = Job(os.path.join(path, 'hf2'))
    hf_result = Results.Result(hf_job, energy=hf_e, unit=hf_unit)
    # embedded fragment LdrCCD (RPA)
    rpa_e, rpa_unit = read_data_from_json(results_file, ['rpa', 'energy', 'layer_energy'])
    rpa_job = Job(os.path.join(path, 'rpa'))
    rpa_result = Results.Result(rpa_job, rpa_e, rpa_unit)

    # final results
    final_data = {}
    # print(hf_result)
    # print(rpa_result)
    # print(extrap_method_error)
    # print(basis_set_correction)
    if 'avdtz' in extrap_method_error and 'avdtz' in basis_set_correction:
        avdtz = hf_result + rpa_result + extrap_method_error['avdtz'] + basis_set_correction['avdtz']
        final_data['avdtz'] = avdtz
    if 'avtqz' in extrap_method_error and 'avtqz' in basis_set_correction:
        avtqz = hf_result + rpa_result + extrap_method_error['avtqz'] + basis_set_correction['avtqz']
        final_data['avtqz'] = avtqz
    for key, value in final_data.items():
        value.record_data_json(['final result', key])

    # if needed, converte unit
    curr_unit = find_current_unit(final_data)
    if curr_unit.lower() != unit.lower():
        for value in final_data.values():
            value.energy = unit_transform(value.energy, curr_unit, unit)
            value.unit = unit
        for key, value in final_data.items():
            value.record_data_json(['final result', key])

    rec = 'Data processing finished!\n'
    rec += '***'*25
    print(rec)
    record(path, rec)


def find_current_unit(results_dict):
    for value in results_dict.values():
        unit = value.unit
        if len(unit) > 0:
            return unit


def get_jobs(path):
    path = os.path.join(path, 'cluster')
    walks = os.walk(path)
    jobs = set()
    root_jobs = set()
    for root, dirs, files in walks:
        if len(files) > 0:
            for file in files:
                if os.path.splitext(file)[-1] == '.out':
                    new_job = Job(root)
                    new_job.method = os.path.splitext(file)[0]
                    if if_cal_finish(new_job) and new_job not in jobs:
                        new_job.bs = get_bs_in_job(new_job)
                        jobs.add(new_job)
                        root_jobs.add(Job(root))
    jobs = list(jobs)
    root_jobs = list(root_jobs)
    return jobs, root_jobs


def get_bs_in_job(job):
    method = job.method
    bs = method.split('_')[0]
    return bs


def if_read_record_results_needed(jobs, results_file):
    """
    check if all results of correction calculation is read and recorded.
    :param jobs:
    :param results_file:
    :return:
    """
    try:
        with open(results_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError as e:
        print(e)
        return True
    try:
        correction_data = data['correction']['energy']
        for job in jobs:
            if job.method not in correction_data:
                return True
        return False
    except KeyError as e:
        print(e)
        return True


def read_data_from_json(json_file, items):
    """
    read data from 'results.json'
    :param json_file: the path of 'results.json'
    :param items: the items in the hierarchy of reserved data
    :return:
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    for i in range(len(items)):
        if i == 0:
            value = data[items[0]]
        else:
            value = value[items[i]]
    return value


if __name__ == '__main__':
    path = r'C:\Users\ccccc\PycharmProjects\single_point\test'
    results(path)
