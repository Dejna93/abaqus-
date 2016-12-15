class Config(object):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            self.__dict__[key] = value

        self.window_width = 350
        self.window_height = 600

        self.odb_path = ''
        self.odb_name = ''
        self.odb_fullpath = ''



config = Config()
