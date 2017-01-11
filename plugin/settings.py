
class Config(object):
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
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.odb = ''

        self._vars2D = ("S", "PEEQ", "EVOL", "SDV121", "U", "T", "UR3", "RF", "RM3")
        self._vars3D = ("T", "D", "S")

        self.vars2D = []
        self.vars3D = []

        self.selected_vars = []

        self.selected_vars_kind = "2D"

        self.parts = {}  # get dict of parts

        self.steps = 0

        self.values = 0

        self.values_counter = 0
        self.elements_counter = 0
        self.frameCounter = 0
        self.parts = {}

        self.increments = [0, self.values_counter]
        self.material_range = [0, self.values_counter]

config = Config()
global_vars_storage = GlobalVarsStorage()
