import os
import tkMessageBox
from plugin.settings import config
from plugin.settings import global_vars_storage

from abaqus import *
from odbAccess import openOdb
import visualization


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class OdbReader(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.odb_name = ""
        self.odb_path = ""

    def __str__(self):
        return "OdbFile: %s" % self.odb_name

    def __unicode__(self):
        return "OdbFile: %s" % self.odb_name

    def get_odb(self):
        try:
            odbFile = openOdb(name=str(os.path.join(self.odb_path, self.odb_name)), readOnly=True)
        except Exception as e:
            tkMessageBox.showerror("Invalid ODB", "This file is corrupted or it is not ODB file.\n"
                                                  "Please, submit valid file!\n\n"
                                                  "ErrorDetails: %s" % e)
            return None
        else:
            return odbFile

    def collect_gui_variables(self):
        # odb_file = self.get_odb()
        storage = global_vars_storage
        odb_file = session.openOdb(name=str(os.path.join(self.odb_path, self.odb_name)), readOnly=True)
        # storage.frameCounter = len(odb_file.steps.values()[0].frames)
        # storage.valuesCounter = len(odb_file.steps.values())

        storage.vars_2D = set(list(odb_file.steps.values()[0].frames[0].fieldOutputs.keys())) & set(global_vars_storage._vars2D)
        storage.vars_3D = set(list(odb_file.steps.values()[0].frames[0].fieldOutputs.keys())) & set(global_vars_storage._vars3D)

        storage.steps = list(str(odb_file.steps.keys()))
        storage.parts = list(odb_file.rootAssembly.instances.keys())  # This way may can not work :-)

        odb_file.close()


odb_reader = OdbReader()
