import sys
import sprint
import unittest
import networkx as n
from coordinator.engine import  Coordinator
import environment
import stdlib

class test_link_order(unittest.TestCase):

    def setUp(self):

        # initialize environment variables
        environment.getEnvironmentVars()

        if sys.gettrace():
            print 'Detected Debug Mode'
            # initialize debug listener (reroute messages to console)
            self.d = sprint.DebugListener()

        self.engine = Coordinator()
        sprint.PrintTarget.CONSOLE = 1134

        self.g = n.DiGraph()

    def tearDown(self):
        del self.g

    def test_determine_execution_order(self):

        # add models
        mdl1 = '../data/randomizer.mdl'
        mdl2 = '../data/multiplier.mdl'

        # add both models.  ids can be anything
        id1 = 'm1'
        id2 = 'm2'
        m1 = self.engine.add_model(id=id1, attrib={'mdl': mdl1})
        m2 = self.engine.add_model(id=id2, attrib={'mdl': mdl2})
        self.assertTrue(m1)
        self.assertTrue(m2)
        self.assertTrue(len(self.engine.Models()) == 2)

        # create link
        rand_oei =  self.engine.get_exchange_item_info(modelid=id1, eitype=stdlib.ExchangeItemType.OUTPUT)
        mult_iei = self.engine.get_exchange_item_info(modelid=id2, eitype=stdlib.ExchangeItemType.INPUT)
        self.engine.add_link(from_id=id1, from_item_id=rand_oei[0]['name'],
                             to_id=id2, to_item_id=mult_iei[0]['name'],
                             spatial_interp=None,
                             temporal_interp=None,
                             uid=None)

        self.assertTrue(len(self.engine.get_all_links()) == 1)


        # get execution order
        order = self.engine.determine_execution_order()

        self.assertTrue(''.join(order) == 'm1m2')

    def test_basic(self):
        """

        m1 -> m2 -> m3 -> m4 -> m5 -> m6
        """

        # add some edges to simulate links
        self.g.add_edge('m1','m2')
        self.g.add_edge('m2','m3')
        self.g.add_edge('m3','m4')
        self.g.add_edge('m4','m5')
        self.g.add_edge('m5','m6')

        order = n.topological_sort(self.g)

        self.assertTrue(''.join(order) == 'm1m2m3m4m5m6')


    def test_simple_tree(self):
        """
              m1 -> m2
                        -> m3
        m6 -> m5 -> m4
        """
        self.g.add_edge('m1','m2')
        self.g.add_edge('m2','m3')

        self.g.add_edge('m6','m5')
        self.g.add_edge('m5','m4')
        self.g.add_edge('m4','m3')


        order = n.topological_sort(self.g)

        self.assertTrue(''.join(order) == 'm1m2m6m5m4m3')

    def test_loop(self):
        """

        m6 -> m5 -> m4 \
        ^               \
        |                -> m3
         <- |m1| -> m2 /

        """

        self.g.add_edge('m1','m2')
        self.g.add_edge('m1','m6')

        self.g.add_edge('m2','m3')
        self.g.add_edge('m6','m5')
        self.g.add_edge('m5','m4')
        self.g.add_edge('m4','m3')

        order = n.topological_sort(self.g)

        self.assertTrue(''.join(order) == 'm1m2m6m5m4m3')

    def test_bidirectional(self):
        """
         m1 <-> m2 -> m3

        """


        self.g.add_edge('m1','m2')
        self.g.add_edge('m2','m3')
        self.g.add_edge('m3','m2')
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

