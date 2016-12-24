# from plugin.odb_scripts.source import OdbFile
class Config(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.window_width = 350
        self.window_height = 600

        self.odb_path = ''
        self.odb_name = ''
        self.odb_fullpath = ''

        # self.odbFile = OdbFile()


class GlobalVarsStorage(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.vars2D = ("S", "PEEQ", "EVOL", "SDV121", "U", "T", "UR3", "RF", "RM3")
        self.vars3D = ("T", "D", "S")

        self.steps = 0

        self.increments_counter = 0
        self.elements_counter = 0
        self.parts = 0
config = Config()
global_vars_storage = GlobalVarsStorage()
