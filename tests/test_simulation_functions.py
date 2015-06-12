# __author__ = 'tonycastronova'

# """
# This file consists of functions designed to test simulation-based functions.
# """

# import unittest
# import coordinator.engineAccessors as engine
# import os
# import time
# from gui.controller.logicCanvas import LogicCanvas
# import wx




#     # def test_something(self):
#     #     frame= wx.Frame(None)
#     #     frame.Show()
#     #
#     #
#     # def test_something_else(self):
#     #     frame= wx.Frame(None)
#     #     frame.Show()
#     #     self.app.MainLoop()




# class TestSimulationFunctions(unittest.TestCase):

#     def setUp(self):
#         self.app= wx.App(False)
#         self.frame = wx.Frame(None, wx.ID_ANY, "Hello World") # A Frame is a top-level window.
#         self.canvas = LogicCanvas(parent=self.frame)

#     def tearDown(self):
#         wx.CallAfter(self.app.Exit)
#         self.app.MainLoop()

#     def test_save_feed_forward(self):

#         print engine.getAllModels()

#         # load the model within the engine process
#         model_path = os.path.join(os.getcwd(), '../models/test_models/randomizer/randomizer.mdl')
#         self.canvas.addModel(model_path,1,1)

#         model_path = os.path.join(os.getcwd(), '../models/test_models/multiplier/multiplier.mdl')
#         self.canvas.addModel(model_path,1,1)
#         time.sleep(1)

#         # save simulation
#         outfile = os.path.join(os.getcwd(), './test_save_simulation.sim')
#         self.canvas.SaveSimulation(outfile)

#         # validate
#         self.assertTrue(os.path.exists(outfile))
#         os.remove(outfile)

#         self.canvas.clear()
#         time.sleep(1)

#         self.assertTrue(engine.getAllModels() == [])

#     def test_save_models_and_links(self):

#         # load the model within the engine process
#         model_path = os.path.join(os.getcwd(), '../models/test_models/randomizer/randomizer.mdl')
#         m1 = self.canvas.addModel(model_path,1,1)

#         model_path = os.path.join(os.getcwd(), '../models/test_models/multiplier/multiplier.mdl')
#         m2 = self.canvas.addModel(model_path,1,1)
#         time.sleep(1)

#         M1 = engine.getModelById(m1)
#         M2 = engine.getModelById(m2)

#         O = engine.getOutputExchangeItems(m1)[0]['name']
#         I = engine.getInputExchangeItems(m2)[0]['name']

#         engine.addLink(M1['id'],O,
#                        M2['id'],I)


#         # save simulation
#         outfile = os.path.join(os.getcwd(), './test_save_simulation.sim')
#         self.canvas.SaveSimulation(outfile)

#         # validate
#         self.assertTrue(os.path.exists(outfile))
#         os.remove(outfile)

#         self.canvas.clear()
#         time.sleep(1)

#         self.assertTrue(engine.getAllModels() == [])

#     def test_load_simulation(self):

#         # load the model within the engine process
#         model_path = os.path.join(os.getcwd(), '../models/test_models/randomizer/randomizer.mdl')
#         m1 = self.canvas.addModel(model_path,1,1)

#         model_path = os.path.join(os.getcwd(), '../models/test_models/multiplier/multiplier.mdl')
#         m2 = self.canvas.addModel(model_path,1,1)
#         time.sleep(1)

#         M1 = engine.getModelById(m1)
#         M2 = engine.getModelById(m2)

#         O = engine.getOutputExchangeItems(m1)[0]['name']
#         I = engine.getInputExchangeItems(m2)[0]['name']

#         engine.addLink(M1['id'],O,
#                        M2['id'],I)


#         # save simulation
#         outfile = os.path.join(os.getcwd(), './test_save_simulation.sim')
#         self.canvas.SaveSimulation(outfile)

#         # validate
#         self.assertTrue(os.path.exists(outfile))

#         # clear the canvas
#         self.canvas.clear()

#         # load simulation
#         self.canvas.loadsimulation(outfile)

#         M1 = engine.getModelById(m1)
#         M2 = engine.getModelById(m2)
#         L = engine.getAllLinks()

#         # validate
#         self.assertTrue(M1 is not None)
#         self.assertTrue(M2 is not None)
#         self.assertTrue(L is not None)

#         os.remove(outfile)

#         self.canvas.clear()
#         time.sleep(1)

#         self.assertTrue(engine.getAllModels() == [])

# if __name__ == "__main__":
#     unittest.main()