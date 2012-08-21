#!/usr/bin/python

from setuptools import setup, find_packages

from docs import longdesc
import codicefiscale

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
       long_description = longdesc,
       test_suite = "tests"
)
