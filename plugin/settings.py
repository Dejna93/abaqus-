class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(object):
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.window_width = 350
        self.window_height = 600

        self.odb_path = ''
        self.odb_name = ''
        self.odb_fullpath = ''

        self.output_path = '.'

        self.req = ("futures", "matplotlib")


class GlobalVarsStorage(object):
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.odb_path = ''

        self._vars2D = ("S", "PEEQ", "EVOL", "SDV121", "U", "T", "UR3", "RF", "RM3")
        self._vars3D = ("T", "D", "S")

        self.vars2D = []
        self.vars3D = []

        self.selected_vars = []

        self.selected_vars_kind = "2D"

        self.parts = {}  # get dict of parts

        self.steps = ""
        self.parts = ""

        self.increments_range = 0
        self.material_range = 0

config = Config()
global_vars_storage = GlobalVarsStorage()
