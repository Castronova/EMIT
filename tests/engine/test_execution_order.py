__author__ = 'tonycastronova'


import unittest
import networkx as n
import time
from coordinator.engine import  Coordinator

class test_link_order(unittest.TestCase):

    def setUp(self):

        self.g = n.DiGraph()
        self.engine = Coordinator()

    def tearDown(self):
        del self.g

    def test_determine_execution_order(self):

        # add models
        mdl1 = '../models/test_models/randomizer/randomizer.mdl'
        mdl2 = '../models/test_models/multiplier/multiplier.mdl'

        # add both models.  ids can be anything
        id1 = 'id:randomizer'
        id2 = 'id:multiplier'
        self.engine.add_model(id=id1, attrib={'mdl': mdl1})
        self.engine.add_model(id=id2, attrib={'mdl': mdl2})
        time.sleep(1)

        # create link
        linkid = self.engine.add_link(id1,'random 1-10',id2,'some_value')
        time.sleep(1)

        # get execution order
        order = self.engine.determine_execution_order()

        self.assertTrue(order.index(id1) > order.index(id2))

    def test_basic(self):
        """

        m1 -> model -> m3 -> m4 -> m5 -> m6
        """

        # add some edges to simulate links
        self.g.add_edge('m1','model')
        self.g.add_edge('model','m3')
        self.g.add_edge('m3','m4')
        self.g.add_edge('m4','m5')
        self.g.add_edge('m5','m6')

        order = n.topological_sort(self.g)

        self.assertTrue(''.join(order) == 'm1m2m3m4m5m6')

        #self.sim.__linknetwork = g

    def test_simple_tree(self):
        """
              m1 -> model
                        -> m3
        m6 -> m5 -> m4
        """
        self.g.add_edge('m1','model')
        self.g.add_edge('model','m3')

        self.g.add_edge('m6','m5')
        self.g.add_edge('m5','m4')
        self.g.add_edge('m4','m3')


        order = n.topological_sort(self.g)

        self.assertTrue(order.index('m1') < order.index('model'))
        self.assertTrue(order.index('m6') < order.index('m5'))
        self.assertTrue(order.index('m5') < order.index('m4'))
        self.assertTrue(order.index('m3') == 5)


    def test_loop(self):
        """

        m6 -> m5 -> m4 \
        ^               \
        |                -> m3
         <- |m1| -> model /

        """

        self.g.add_edge('m1','model')
        self.g.add_edge('m1','m6')

        self.g.add_edge('model','m3')
        self.g.add_edge('m6','m5')
        self.g.add_edge('m5','m4')
        self.g.add_edge('m4','m3')

        order = n.topological_sort(self.g)

        self.assertTrue(order.index('m1') == 0)
        self.assertTrue(order.index('m6') < order.index('m5'))
        self.assertTrue(order.index('m5') < order.index('m4'))
        self.assertTrue(order.index('m3') == 5)

    def test_bidirectional(self):
        """
         m1 <-> model -> m3

        """


        self.g.add_edge('m1','model')
        self.g.add_edge('model','m3')
        self.g.add_edge('m3','model')
        self.g.add_edge('m3','m4')

        # remove any models that done have links
        #for

        # determine cycles
        cycles = n.recursive_simple_cycles(self.g)
        for cycle in cycles:
            # remove edges that form cycles
            self.g.remove_edge(cycle[0],cycle[1])

        # perform toposort
        order = n.topological_sort(self.g)

        # re-add bidirectional dependencies (i.e. cycles)
        for cycle in cycles:
            # find index of inverse link
            for i in xrange(0,len(order)-1):
                if order[i] == cycle[1] and order[i+1] == cycle[0]:
                    order.insert(i+2, cycle[1])
                    order.insert(i+3,cycle[0])
                    break

        self.assertTrue(''.join(order) == 'm1m2m3m2m3m4')

