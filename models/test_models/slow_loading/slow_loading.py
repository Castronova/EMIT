__author__ = 'tonycastronova'

from wrappers import feed_forward



class slowloading(feed_forward.feed_forward_wrapper):

    def __init__(self,config_params):
        super(slowloading, self).__init__(config_params)

        # loop designed to cause slow initialization
        cnt = 0
        for i in range(0,50000000):
            cnt += i


    def run(self,inputs):

        pass

    def save(self):
        """
        This function is used to build output exchange items
        :return: list of output exchange items
        """

        return []