import os

try:
    from abaqus import *
    from abaqusConstans import *
    import visualization

except Exception:
    print("Odpalane zdala od bambaqusa")

from plugin.settings import config

Path = config.odb_path
odbFile = config.odb_fullpath


def test():
    odb = session.openOdb(name=str(os.path.join(config.odb_path, config.odb_name)))
    print("Test step print")
    print (len(odb.steps))

    values = odb.steps.values()
    print("Valies", values)
    for i in range(len(values[0].frames)):
        S = values[0].frames[i].fieldOutputs['S']
        print("S:", S)
        for j in range(len(values[0].frames[0].fieldOutputs['S'].values)):
            print "S elementlabel ", (str(S.values[j].elementLabel - 1))
            print "S mises ", (str(S.values[j].mises))

class OdbFile(object):
    def __init__(self):
        self.odb = session.openOdb(name=str(os.path.join(config.odb_path, config.odb_name)))