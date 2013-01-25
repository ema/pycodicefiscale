#!/usr/bin/python

"""codicefiscale's setup script.

A new version can be built and uploaded to pypi as follows:

$ python setup.py bdist_egg sdist upload
"""

from setuptools import setup

import codicefiscale

LONGDESC = codicefiscale.__doc__

LONGDESC = """%s

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
""" % LONGDESC

for what in dir(codicefiscale):
    if not what.startswith("__"):
        obj = getattr(codicefiscale, what)
        if callable(obj) and obj.__doc__:
            LONGDESC += obj.__doc__ + "\n\n\n"

setup(
       name = 'codicefiscale',
       author = codicefiscale.__author__,
       author_email = 'ema@linux.it',
       url='https://github.com/ema/pycodicefiscale',
       download_url='https://github.com/ema/pycodicefiscale/downloads',
       version = codicefiscale.__version__,
       py_modules = ['codicefiscale'],
       zip_safe = True,
       license='LGPL',
       description="Python library for Italian fiscal code (codicefiscale)",
       long_description = LONGDESC,
       test_suite = "tests"
)
