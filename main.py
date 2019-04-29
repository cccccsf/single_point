#!/usr/bin/python3
import shutil
from datetime import datetime
from Components import IniReader
from OsComponents import mkdir
from OsComponents import record
from OsComponents import rename_file
import GeoOpt
import HF1
import Loc
import HF2
import LMP2
import RPA
import Cluster


def pipeline():

    Ini = IniReader()
    path = Ini.project_path
    start = Ini.start
    end = Ini.end

    now = datetime.now()
    now = now.strftime("%b %d %Y %H:%M:%S")
    rec = 'Project begins.'
    rec += '\n' + '***'*25
    rename_file(path, 'record')
    record(path, rec, init=True)
    print(now)
    print(rec)
    mkdir(path)
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
        elif anchor == 4:
            LMP2.lmp2(path)
        elif anchor == 5:
            RPA.rpa(path)
        elif anchor == 6:
            Cluster.cluster(path)
    #     elif anchor == 7:
    #         Correction.correction(path)
        anchor += 1

    now = datetime.now()
    now = now.strftime("%b %d %Y %H:%M:%S")
    rec = 'Project End.\n'
    rec += '***'*25
    rename_file(path, 'record')
    record(path, rec, init=True)
    print(now)
    print(rec)


if __name__ == "__main__":
    pipeline()
