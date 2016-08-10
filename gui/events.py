__author__ = 'tonycastronova'

from eventbase import EventHook

# Simulation Save & Load Events
onSaveFromCanvas = EventHook('onSaveFromCanvas')

# Database Related Events
onDbChanged = EventHook('on_database_changed')


#  Pre Run Events
onClickRun = EventHook('onClickRun')
