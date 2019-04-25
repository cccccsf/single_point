#!/usr/bin/python3
import shutil
from Components import IniReader
from OsComponents import mkdir
from OsComponents import record
from OsComponents import rename_file
import GeoOpt
import HF1
import Loc
import HF2


def pipeline():

    Ini = IniReader()
    path = Ini.project_path
    start = Ini.start
    end = Ini.end

    mkdir(path)
    rec = 'Project begins.'
    rec += '\n' + '***'*25
    rename_file(path, 'record')
    record(path, rec, init=True)
    try:
        shutil.copy(Ini.ini_path, path+'/input.ini')
    except Exception as e:
        print(e)
        
    anchor = start
    while anchor < end:
        # print(anchor, end)
        if anchor == 0:
            GeoOpt.geo_opt(path)
        elif anchor == 1:
            HF1.hf1(path)
        elif anchor == 2:
            Loc.localization(path)
        elif anchor == 3:
            HF2.hf2(path)
    #     elif anchor == 4:
    #         LMP2.lmp2(path)
    #     elif anchor == 5:
    #         RPA.rpa(path)
    #     elif anchor == 6:
    #         CLUSTER.cluster(path)
    #     elif anchor == 7:
    #         Correction.correction(path)
        anchor += 1
    # end_programm(path)


if __name__ == "__main__":
    pipeline()
