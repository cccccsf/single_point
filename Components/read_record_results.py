#!/usr/bin/python3
from Components import cal_layer_energy
from Components import record_data_json
from Components import record_data_csv
from OsComponents import record


def read_record_results(path, jobs, energy_func, method='hf'):
    energy_dict = {}
    for job in jobs:
        if job.layertype == 'bilayer':
            energy, unit = energy_func(job)
            energy = [energy, unit]
            energy_dict['bilayer'] = energy
        elif job.layertype == 'upperlayer':
            energy, unit = energy_func(job)
            energy = [energy, unit]
            energy_dict['upperlayer'] = energy
        elif job.layertype == 'underlayer':
            energy, unit = energy_func(job)
            energy = [energy, unit]
            energy_dict['underlayer'] = energy
    layer_energy = cal_layer_energy(
        energy_dict['bilayer'],
        energy_dict['upperlayer'],
        energy_dict['underlayer'])
    energy_dict['layer_energy'] = layer_energy
    record_data_json(path, 'energy', energy_dict, section=method)
    record_data_csv(path,
                    method,
                    [energy_dict['bilayer'][0],
                     energy_dict['upperlayer'][0],
                        energy_dict['underlayer'][0],
                        energy_dict['layer_energy'][0]],
                    layer='whole layer')
    rec = method + 'Results readed.\n'
    rec += '---' * 25
    print(rec)
    record(path, rec)
