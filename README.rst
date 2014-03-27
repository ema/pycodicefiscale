Python library for Italian fiscal code

.. image:: https://secure.travis-ci.org/ema/pycodicefiscale.png?branch=master
   :target: http://travis-ci.org/ema/pycodicefiscale 

codicefiscale is a Python library for working with Italian fiscal code numbers
officially known as Italy's Codice Fiscale.

Copyright (C) 2009-2013 Emanuele Rocca

Homepage: https://github.com/ema/pycodicefiscale

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
``build(surname, name, birthday, sex, municipality) -> string``

    Computes the fiscal code for the given person data.

    eg: build('Rocca', 'Emanuele', datetime.datetime(1983, 11, 18), 'M', 'D969') 
        -> RCCMNL83S18D969H
    


``control_code(input_string) -> int``

    Computes the control code for the given input_string string. The expected
    input_string is the first 15 characters of a fiscal code.

    eg: control_code('RCCMNL83S18D969') -> 'H'
    


``get_birthday(code) -> string``

    Birthday of the person whose fiscal code is 'code', in the format DD-MM-YY. 

    Unfortunately it's not possible to guess the four digit birth year, given
    that the Italian fiscal code uses only the last two digits (1983 -> 83).
    Therefore, this function returns a string and not a datetime object.

    eg: birthday('RCCMNL83S18D969H') -> 18-11-83
    


``get_sex(code) -> string``

    The sex of the person whose fiscal code is 'code'.

    eg: sex('RCCMNL83S18D969H') -> 'M'
        sex('CNTCHR83T41D969D') -> 'F'


``get_municipality(code) -> string``

    The municipality of the person whose fiscal code is 'code'.

    eg: sex('RCCMNL83S18D969H') -> 'GENOVA'
        sex('CNTCHR83T41D969D') -> 'GENOVA'


``isvalid(code) -> bool``

    This function checks if the given fiscal code is syntactically valid.

    eg: isvalid('RCCMNL83S18D969H') -> True
        isvalid('RCCMNL83S18D969') -> False

