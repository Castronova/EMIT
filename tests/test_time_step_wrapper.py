# __author__ = 'tonycastronova'

# import unittest
# import random
# from shapely.wkt import loads
# from wrappers import time_step
# import copy
# from stdlib import ElementType,Geometry, ExchangeItem, ExchangeItemType, DataValues
# import datetime
# import time
# import matplotlib.pyplot as plt

# class testTimeStepWrapper(unittest.TestCase):

#     def setUp(self):

#         self.pts = []

#         for i in range (0,100):

#             x = random.randint(0, 10000)
#             y = random.randint(0, 10000)
#             wkt = 'POINT(%3.5f %3.5f)' % (x,y)

#             geom = Geometry(datavalues=DataValues())
#             geom.set_geom_from_wkt(wkt)


#             self.pts.append(geom)

#         params = {}
#         params['model'] = [{'code':'None'}]
#         params['model'] = [{'description':'None'}]

#         self.ts = time_step.time_step_wrapper(params)

#         self.ei = ExchangeItem(id=1,
#                           name='test',
#                           desc='none',
#                           geometry=self.pts,
#                           unit=None,
#                           variable='test_variable',
#                           type=ExchangeItemType.Output)

#         outs = self.ts.outputs(value=[self.ei])


#     def test_set_geom_values(self):

#         datavalues = zip([datetime.datetime.today()],[10])

#         pts = copy.copy(self.pts)
#         st = time.time()
#         while len(pts) > 0:
#             idx = random.randint(0,len(pts)-1)
#             pt = pts.pop(idx)
#             self.ts.set_geom_values('test',pt,datavalues)
#         t1 = time.time() - st
#         print 'Elapsed time %3.5f seconds ' % t1



#         pts = copy.copy(self.pts)
#         st = time.time()

#         while len(pts) > 0:
#             idx = random.randint(0,len(pts)-1)
#             pt = pts.pop(idx)
#             self.ts.set_geom_values_by_hash('test',pt,datavalues)
#         t2 = time.time() - st
#         print 'Elapsed time %3.5f seconds ' %t2



#     def test_speed_up(self):

#         element_set_size = [100,200,400,800,1600,3200]
#         t1s = []
#         t2s = []

#         for size in element_set_size:

#             self.pts = []

#             for i in range (0,size):

#                 x = random.randint(0, 10000)
#                 y = random.randint(0, 10000)
#                 wkt = 'POINT(%3.5f %3.5f)' % (x,y)

#                 geom = Geometry(datavalues=DataValues())
#                 geom.set_geom_from_wkt(wkt)


#                 self.pts.append(geom)

#             params = {}
#             params['model'] = [{'code':'None'}]
#             params['model'] = [{'description':'None'}]

#             self.ts = time_step.time_step_wrapper(params)

#             self.ei = ExchangeItem(id=1,
#                               name='test',
#                               desc='none',
#                               geometry=self.pts,
#                               unit=None,
#                               variable='test_variable',
#                               type=ExchangeItemType.Output)

#             outs = self.ts.outputs(value=[self.ei])



#             print 'Evaluating ',size,' Elements...',

#             datavalues = zip([datetime.datetime.today()],[10])

#             pts = copy.copy(self.pts)
#             st = time.time()
#             while len(pts) > 0:
#                 idx = random.randint(0,len(pts)-1)
#                 pt = pts.pop(idx)
#                 self.ts.set_geom_values('test',pt,datavalues)
#             t1 = time.time() - st
#             t1s.append(t1)


#             pts = copy.copy(self.pts)
#             st = time.time()

#             while len(pts) > 0:
#                 idx = random.randint(0,len(pts)-1)
#                 pt = pts.pop(idx)
#                 self.ts.set_geom_values_by_hash('test',pt,datavalues)
#             t2 = time.time() - st
#             t2s.append(t2)

#             print ' %3.3f sec --> %3.3f sec ' % (t1,t2)


#         plt.plot(element_set_size, t1s, 'yo-', label='Old Data Setting Method')
#         plt.plot(element_set_size, t2s, 'ro-', label='New Data Setting Method')
#         plt.xlabel('Element Set Size')
#         plt.ylabel('Execution Time (seconds)')
#         plt.legend()
#         plt.grid(True)
#         plt.show()


