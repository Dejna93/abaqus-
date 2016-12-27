import os
import threading

try:
    from abaqus import *
    from abaqusConstans import *
    import visualization

except Exception:
    pass

from plugin.settings import config
from plugin.settings import global_vars_storage

class OdbFile(object):
    def __init__(self, odbFile, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.odb = odbFile
        self.parts = {}
        self.max_step = 0
        self.increments_counter = 0
        self.elements_counter = 0
        self.output2D_variables = []
        self.output3D_variables = []

        self.valuesCounter = ''
        self.frameCounter = 0

    def __unicode__(self):
        return str("File name: %s" % config.odb_name)

    def collect_variables(self):
        values = self.odb.steps.values()
        """
            This function will try to get all avaliavle
            variables from odbfile and update gui.
        """
        for var in global_vars_storage._vars2D:
            print(var)
            try:
                temp = values[0].frames[0].fieldOutputs[var]
            except Exception:
                continue
            else:
                self.output2D_variables.append(var)

        for var in global_vars_storage._vars3D:
            try:
                temp = values[0].frames[0].fieldOutputs[var]
            except Exception:
                continue
            else:
                self.output3D_variables.append(var)

        self.max_step = len(self.odb.steps)

        self.valuesCounter = self.odb.steps.values()
        self.frameCounter = len(values[0].frames)

    def get_parts(self):
        for key, value in self.odb.steps.items():
            self.parts[key] = value
        return self.parts

    def update_global_storage(self):
        """
        :return: Update global variables storage
        """
        storage = global_vars_storage
        self.collect_variables()
        storage.parts = self.get_parts()
        storage.steps = self.max_step
        storage.vars2D = self.output2D_variables
        storage.vars3D = self.output3D_variables

        print(self.output2D_variables)

class SaveOutput(object):
    def __init__(self):
        self.threads = []
        self.output_files = []

    def create_output(self):
        thread_inc = threading.Thread(target=self.save_increments)
        thread_el = threading.Thread(target=self.save_elements)

        self.threads.append(thread_inc)
        self.threads.append(thread_el)
        thread_inc.start()
        thread_el.start()

    def save_increments(self):
        pass

    def save_elements(self):
        pass

    def collect_options(self):
        pass