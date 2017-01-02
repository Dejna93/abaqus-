import os
import threading
import tkMessageBox
import multiprocessing

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


class SaveOutput(object):
    def __init__(self):
        self.output_files = []

        self.materials_txt_file = ''
        self.increments_txt_file = ''

        self.storage = global_vars_storage

    def create_file(self):
        jobs = []
        step = self.storage.frameCounter/multiprocessing.cpu_count() + \
               self.storage.frameCounter%multiprocessing.cpu_count() > 0  # rounding up!
        int(21 / 5) + (21 % 5 > 0)
        print ("P %s S %s" % (multiprocessing.cpu_count(), self.storage.frameCounter))
        print ("Step: ", step)
        print "Create file"
        for start in range(0, self.storage.frameCounter, step):
            end = start+step
            if start+step > self.storage.frameCounter:
                end = self.storage.frameCounter
            rang = (start, end)
            print "range: ", rang
            p = threading.Process(target=self.save_file, args=(rang,))
            jobs.append(p)
            print "Starting process"
            p.start()

        for job in jobs:

            job.join()

    def save_file(self, range):
        """
        :param range: It is for range (framecounter) for every running proces (parallelism)
        :return: Nothing, it is only save file
        """
        values = self.storage.odb.steps.values()
        values_dict = {}
        if self.storage.selected_vars_kind == "2D":
            for frame in range(range):  # parallelism, range eg [0,15]
                output_file = os.path.join(config.output_path, "Increment%s.txt" % frame)
                print "Tworzenie pliku\nPath: %s" % output_file
                with open(output_file, mode='w') as file:
                    for var in self.storage.selected_vars2D:
                        values_dict[var] = values[0].frames[frame].fieldOutputs[var]
                    for j in range(0, self.storage.values_counter):
                        output_string = '%d' % j
                        for key, value in values_dict.items():
                            if key == "S":
                                output_string += ":%s" % value.values[j].elementLabel-1
                                output_string += ":%s" % value.values[j].mises
                            output_string += ":%s" % value.values[j].data
                    file.write(output_string+'\n')

        if self.storage.selected_vars_kind == "3D":
            for frame in range(range):  # parallelism, range eg [0,15]
                output_file = os.path.join(config.output_path, "Increment%s.txt" % frame)
                with open(output_file, mode='w') as file:
                    for var in self.storage.selected_vars3D:
                        values_dict[var] = values[0].frames[frame].fieldOutputs[var]
                    for j in range(0, self.storage.values_counter):
                        output_string = '%d' % j
                        for key, value in values_dict.items():
                            if key == "S":
                                output_string += ":%s" % value.values[j].elementLabel - 1
                                output_string += ":%s" % value.values[j].mises
                            output_string += ":%s" % value.values[j].data
                            self.write_file("%s.txt" % frame, output_string)
                        file.write(output_string + '\n')

save_out = SaveOutput()