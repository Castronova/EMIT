__author__ = 'tonycastronova'

import wrappers
from wrappers import base

class WofWrapper(base.BaseWrapper):


    def __init__(self, args):
        super(WofWrapper, self).__init__(self)

        self.args = args



    def type(self):
        return wrappers.Types().WOF
