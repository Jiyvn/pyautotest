from constant import PROJ
from app.utils.confile import reader


class Loader(object):

    def __init__(self):
        pass

    def get_default_caps(self):
        return self.load(PROJ.CAPS)

    @staticmethod
    def load(file):
        return reader.read(file)
