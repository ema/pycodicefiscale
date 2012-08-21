"""Generate a README file"""

import codicefiscale

longdesc = codicefiscale.__doc__

longdesc = """%s

codicefiscale Module Documentation
==================================

A quick example
---------------
>>> import datetime
>>> from codicefiscale import build
>>>
>>> build('Rocca', 'Emanuele', datetime.datetime(1983, 11, 18), 'M', 'D969')
'RCCMNL83S18D969H'

Module Contents
---------------
""" % longdesc

for what in dir(codicefiscale):
    if not what.startswith("__"):
        obj = getattr(codicefiscale, what)
        if callable(obj) and obj.__doc__:
            longdesc += obj.__doc__ + "\n\n\n"

if __name__ == "__main__":
    print longdesc
