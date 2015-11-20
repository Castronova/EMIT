__author__ = 'tonycastronova'


class Globals():
    def __init__(self):
        self.__globals = {}

    def set(self, name, value):
        self.__globals[name] = value

    def get(self, name):
        return self.__globals[name]