__author__ = 'tonycastronova'

import sys

from sprint import *

class EventResponse:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class EventManager(object):

    # Borg pattern to maintain shared state

    __monostate = None

    def __init__(self):
        if not EventManager.__monostate:
            EventManager.__monostate = self.__dict__
            self.__handlers = {}
            self.__name = id

        else:
            self.__dict__ = EventManager.__monostate

    def add(self, name, handler):
        if name not in self.__handlers.keys():
            self.__handlers[name] = [handler]
        else:
            self.__handlers[name].append(handler)

    def get_handlers(self, name):
        if name in self.__handlers.keys():
            return self.__handlers[name]
        else:
            # ignore if no handlers are assigned, but print warning message to log
            sPrint('No handlers for event %s' % name, MessageType.ERROR)


class EventHook(object):

    def __init__(self, name):
        self.__handlers = {}
        self.__handlers[name] = []
        self.__name = name

    def __iadd__(self, handler):
        evt_mgr = EventManager()
        evt_mgr.add(self.__name, handler)
        self.__handlers[self.__name].append(handler)
        return self

    def __isub__(self, handler):
        raise NotImplementedError()

    def fire(self, **kwargs):

        if sys.gettrace():
            pass
            # sPrint('Event fired: %s' % self.__name, MessageType.INFO)

        # count = 0  # to prevent event firing twice.
        evt_mgr = EventManager()
        handlers = evt_mgr.get_handlers(self.__name)
        if handlers is not None:
            for handler in handlers:
                evt_obj = EventResponse(**kwargs)
                handler(evt_obj)

