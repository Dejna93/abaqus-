import os
import threading
import tkMessageBox
import multiprocessing

from plugin.odb_scripts.save_file import save_file

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
        storage.frameCounter = self.frameCounter
        storage.odb = self.odb
        storage.values = storage.odb.steps.values()
        storage.values_counter = len(storage.values[0].frames[0].fieldOutputs["S"].values)

class SaveOutput(object):
    def __init__(self):
        self.output_files = []

        self.materials_txt_file = ''
        self.increments_txt_file = ''

        self.storage = global_vars_storage

    def create_file(self):

        for i in range(self.storage.frameCounter):
            self.save_increments(i, self.storage)

        self.save_materials(self.storage)

    def save_increments(self, iter, storage):
        """
        :param range: It is for range (framecounter) for every running proces (parallelism)
        :return: Nothing, it is only save file
        """
        values = storage.odb.steps.values()
        values_dict = {}

        print("Working increment %s" % iter)
        if storage.selected_vars_kind == "2D":
            output_dir = os.path.join(config.output_path, config.odb_name.split('.')[0])
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            output_file = os.path.join(output_dir, "Increment%s.txt" % iter)
            with open(output_file, mode='w') as file:
                for var in storage.vars2D:
                    values_dict[var] = values[0].frames[iter].fieldOutputs[var]
                for i in range(0, storage.values_counter):
                    output_string = '%d' % i
                    for key, value in values_dict.items():
                        if key == "S":
                            output_string += ":%s" % str(value.values[i].elementLabel - 1)
                            output_string += ":%s" % value.values[i].mises
                        try:
                            for j in value.values[i].data:
                                output_string += ":%s" % j

                    file.write(output_string + '\n')
            return True

        if storage.selected_vars_kind == "3D":
            return True

        return False

    def save_materials(self, storage):
        output_file = os.path.join(config.output_path, "%s\\materials.txt" % config.odb_name)
        with open(output_file, mode='w') as file:
            file.write("%s:%s" % (storage.values_counter, storage.frameCounter))
            for i in range(storage.material_range):
                file.write("%s:0\n" % i)

save_out = SaveOutput()
