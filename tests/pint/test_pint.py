import numpy as np
from pint import UnitRegistry



def test_basic():

    ureg = UnitRegistry()

    data = np.arange(0,100,.5)

    unit_num = 'cc'
    unit_den = 's'
    unit = ureg[unit_num] / ureg[unit_den]
    print 'from unit: %s' % str(unit)

    # convert data
    to_unit_num = 'l'
    to_unit_den = 'hr'
    print 'to_unit: %s' % str(unit)
    to_unit = ureg[to_unit_num] / ureg[to_unit_den]

    new_data = (data * (unit)).to(to_unit)
    new_data = np.array(new_data)
    for i in range(0, len(data)):
        print '%3.2f (%s) \t\t %3.2f (%s)' % (data[i], str(unit), new_data[i], str(to_unit))



test_basic()