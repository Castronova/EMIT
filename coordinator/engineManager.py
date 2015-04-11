__author__ = 'tonycastronova'

from coordinator.engine import Coordinator


class EngineBorg:
    """
    Borg pattern to ensure that all instances of the engine have shared state
    """

    __monostate = None

    def __init__(self):
        if not EngineBorg.__monostate:
            EngineBorg.__monostate = self.__dict__
            self.engine = Coordinator()

        else:
            self.__dict__ = EngineBorg.__monostate



def get_engine():
    """
    gets the shared engine
    :return: engine coordinator object
    """
    e = EngineBorg()
    return e.engine

