__author__ = 'tonycastronova'


import unittest
import networkx as n

class test_link_order(unittest.TestCase):

    def setUp(self):

        self.g = n.DiGraph()

    def tearDown(self):
        del self.g

    def test_determine_execution_order(self):
        from coordinator import main
        self.sim = main.Coordinator()
        # add models
        mdl1 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/multiplier.mdl'
        id1 = self.sim.add_model(mdl1)
        mdl2 = '/Users/tonycastronova/Documents/projects/iUtah/EMIT/tests/data/random.mdl'
        id2 = self.sim.add_model(mdl2)

        # create link
        linkid = self.sim.add_link(id2,'OUTPUT1',id1,'INPUT1')

        # get execution order
        order = self.sim.determine_execution_order()

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

