
import pint
from pint import UnitRegistry
from sprint import *


def convert_units(oei, iei, vals):

    # Get the stdlib units for input and output exchange items
    oei_std_unit = oei.unit()
    oei_name = oei_std_unit.UnitName()
    oei_abbv = oei_std_unit.UnitAbbreviation()

    iei_std_unit = iei.unit()
    iei_name = iei_std_unit.UnitName()
    iei_abbv = iei_std_unit.UnitAbbreviation()

    # perform unit conversion using the Pint library
    try:

        ureg = UnitRegistry()

        # get pint units
        try:
            iei_pint_unit = ureg[iei_abbv]
        except:
            try:
                iei_pint_unit = ureg[iei_name]
            except:
                raise Exception('Could not convert unit: %s:%s' % (iei_name, iei_abbv))

        try:
            oei_pint_unit = ureg[oei_abbv]
        except:
            try:
                oei_pint_unit = ureg[oei_name]
            except:
                raise Exception('Could not convert unit: %s:%s' % (oei_name, oei_abbv))

        print 'Converting units: %s -> %s' % (oei_pint_unit.units, iei_pint_unit.units)
        conversion_factor = oei_pint_unit.to(iei_pint_unit)
        converted_vals = conversion_factor * vals

    except Exception, e:
        sPrint('Error converting units: %s' % e.message, MessageType.ERROR)
        sPrint('Continuing with "unconverted" units', MessageType.ERROR)
        return vals

    return converted_vals

