__author__ = 'tonycastronova'

from eventbase import EventHook

# Test Events
onChange = EventHook('onChange')
onModified = EventHook('onModified')
onSomething = EventHook('onSomething')


# Model related Events
onModelAdded = EventHook('onModelAdded')
onModelRemoved = EventHook('onModelRemoved')


# Link related Events
onLinkAdded = EventHook('onLinkAdded')
onLinkRemoved = EventHook('onLinkRemoved')
onLinkUpdated = EventHook('onLinkUpdate')


# Simulation related Events
onSimulationFinished = EventHook('onSimulationFinished')
onSimulationError = EventHook('onSimulationError')
onSimulationLoaded = EventHook('onSimulationLoaded')


# Database related Events
onDatabaseConnected = EventHook('onDatabaseConnected')
onDatabaseChanged = EventHook('onDatabaseChanged')


