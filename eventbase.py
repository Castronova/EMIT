__author__ = 'tonycastronova'

from coordinator.emitLogging import elog

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
            elog.warning('No handlers for event: %s', name)

            # raise Exception("No handlers for event: ", name)

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
    #     self.__handlers.remove(handler)
    #     return self

    def fire(self, **kwargs):
        count = 0  # to prevent event firing twice.
        evt_mgr = EventManager()
        handlers = evt_mgr.get_handlers(self.__name)
        if handlers is not None:
            for handler in handlers:
                if count == 0:
                    count = 1
                    evt_obj = EventResponse(**kwargs)
                    handler(evt_obj)

