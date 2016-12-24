import os
try:
    from abaqus import *
    from abaqusConstans import *
    import visualization

except Exception:
    print("Odpalane zdala od bambaqusa")

from plugin.settings import config
from plugin.settings import global_vars_storage

Path = config.odb_path
odbFile = config.odb_fullpath


def test():
    odb = session.openOdb(name=str(
        os.path.join(config.odb_path, config.odb_name)))
    print("Test step print")
    print(len(odb.steps))

    values = odb.steps.values()
    print("Values", values)
    for var in global_vars_storage.vars2D:
        try:
            S = values[0].frames[0].fieldOutputs[var]
        except Exception:
            print "There is no %s value" % var


class OdbFile(object):
    def __init__(self, *args, **kwargs):
        self.odb = session.openOdb(
            name=str(os.path.join(config.odb_path, config.odb_name)))

        for key, value in kwargs.items():
            self.__dict__[key] = value

    def __unicode__(self):
        return str("File name: %s" % config.odb_name)

    def get_steps_from_odb(self):
        return odb.steps

    def get_increments_from_odb(self):
        pass

    def get_elements_from_odb(self):
        pass

    def get_materials_from_odb(self):
        pass


class OdbGuiUpdate(OdbFile):
        def __init__(self, *args, **kwargs):
            OdbFile.__init__(self, *args, **kwargs)

            self.max_step = 0
            self.increments_counter = 0
            self.elements_counter = 0
            self.output2D_variables = []
            self.output3D_variables = []

        def collect_variables(self):
            """
                This function will try to get all avaliavle
                variables from odbfile and update gui.
            """
            for var in global_vars_storage.vars2D:
                try:
                    temp = values[0].frames[0].fieldOutputs[var]
                except Exception:
                    print "There is no %s value" % var
                else:
                    self.output2D_variables.append(var)

            for var in global_vars_storage.vars3D:
                try:
                    temp = values[0].frames[0].fieldOutputs[var]
                except Exception:
                    print "There is no %s value" % var
                else:
                    self.output3D_variables.append(var)

            self.max_step = len(len(odb.steps))
