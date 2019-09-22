#!/usr/bin/python3 

ROOT='/home/pi'
ROOT="."
DEVID_FILE = ROOT+'/deviceid'
RATID_FILE = ROOT+'/ratids'
SESSIONID_FILE = ROOT+'/sessionid'
DATAFILE_PRFX = ROOT+'/Pies/Oxycodone/Oxy_'



class IDS:
    def __init__(self):
        with open (DEVID_FILE) as devID:
            self.devID = str((devID.read()).strip())
            devID.close()
        with open (SESSIONID_FILE) as sessID:
            self.sesID=str(sessID.read().strip())
            sessID.close()
        with open (RATID_FILE) as ratID:
            self.ratID = str((ratID.read()).strip())
            ratID.close()

ids=IDS()
print(ids.devID)
