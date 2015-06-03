__author__ = 'tonycastronova'

from eventbase import EventHook

# Simulation Save & Load Events
onSimulationSaved = EventHook('onSimulationSaved')
onSaveFromCanvas = EventHook('onSaveFromCanvas')

# Database Related Events
onDbChanged = EventHook('onDbChanged')

