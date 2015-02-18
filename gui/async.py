__author__ = 'tonycastronova'

import wx
from threading import Thread
from functools import wraps

def runAsync(func):
    '''Decorates a method to run in a separate thread'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_hl = Thread(target=func, args=args, kwargs=kwargs)
        func_hl.start()
        return func_hl
    return wrapper


def wxCallafter(target):
    '''Decorates a method to be called as a wxCallafter'''
    @wraps(target)
    def wrapper(*args, **kwargs):
        wx.CallAfter(target, *args, **kwargs)
    return wrapper


def threaded(f, daemon=False):
    import Queue

    def wrapped_f(q, *args, **kwargs):
        '''this function calls the decorated function and puts the
        result in a queue'''
        ret = f(*args, **kwargs)
        q.put(ret)

    def wrap(*args, **kwargs):
        '''this is the function returned from the decorator. It fires off
        wrapped_f in a new thread and returns the thread object with
        the result queue attached'''

        q = Queue.Queue()

        t = Thread(target=wrapped_f, args=(q,)+args, kwargs=kwargs)
        t.daemon = daemon
        t.start()
        t.result_queue = q
        return t

    return wrap