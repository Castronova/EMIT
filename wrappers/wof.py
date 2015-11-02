__author__ = 'tonycastronova'

import wrappers
from wrappers import base

class wrapper(base.BaseWrapper):


    def __init__(self, args):
        super(wrapper, self).__init__(self)

        self.args = args



    def type(self):
        return wrappers.Types().WOF
