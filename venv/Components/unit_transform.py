#!/usr/bin/python3

def unit_transform(energy, unit_from, unit_to):

    unit_dict = {
            'ha': 1,
            'hartree': 1,
            'ev': 27.2113839,
            'cm': 219474.63067,
            'kcal/mol': 627.5096,
            'kj/mol': 2625.50,
            'k': 3.157747E5,
            'hz': 6.5796839207E15
        }
    # z.B. here 1 Hartree = 27.2113839 eV

    if unit_from.lower() not in unit_dict or unit_to.lower() not in unit_dict:
        print('Unit not correct.')
        print('Please check and try again.')
        return energy
    else:
        ratio = unit_dict[unit_from.lower()] / unit_dict[unit_to.lower()]
        e = energy / ratio
        return e

# if __name__ == '__main__':
#     energy = 1
#     unit_from = 'ha'
#     unit_to = 'kcal/mol'
#     e = unit_transform(energy, unit_from, unit_to)
#     print(e)
