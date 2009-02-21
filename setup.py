#!/usr/bin/python

from setuptools import setup, find_packages

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

setup(
       name = 'codicefiscale',
       author = codicefiscale.__author__,
       author_email = 'ema@linux.it',
       url='http://code.google.com/p/pycodicefiscale',
       download_url='http://code.google.com/p/pycodicefiscale/downloads/list',
       version = codicefiscale.__version__,
       py_modules = ['codicefiscale'],
       zip_safe = True,
       license='LGPL',
       description="Python library for Italian fiscal code (codicefiscale)",
       long_description = longdesc,
       test_suite = "tests"
)
