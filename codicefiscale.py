"""
Python library for Italian fiscal code

codicefiscale is a Python library for working with Italian fiscal code numbers
officially known as Italy's Codice Fiscale.

Copyright (C) 2009-2013 Emanuele Rocca, eadmaster

Homepage: https://github.com/ema/pycodicefiscale

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

__version__ = '0.9'
__author__ = "Emanuele Rocca, eadmaster"

import re
# pylint: disable=W0402
import string

__VOWELS = [ 'A', 'E', 'I', 'O', 'U' ]
__CONSONANTS = list(set(list(string.ascii_uppercase)).difference(__VOWELS))

MONTHSCODE = [ 'A', 'B', 'C', 'D', 'E', 'H', 'L', 'M', 'P', 'R', 'S', 'T' ]

# pylint: disable=C0301
PATTERN = "^[A-Z]{6}[0-9]{2}([A-E]|[HLMPRST])[0-9]{2}[A-Z][0-9]([A-Z]|[0-9])[0-9][A-Z]$"

import os
MUNICIPALITY_DB_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep + "codici_catastali.csv"


def isvalid(code):
    """``isvalid(code) -> bool``

    This function checks if the given fiscal code is syntactically valid.

    eg: isvalid('RCCMNL83S18D969H') -> True
        isvalid('RCCMNL83S18D969') -> False
    """
    return isinstance(code, basestring) and re.match(PATTERN, code) is not None

# Fiscal code calculation 
def __common_triplet(input_string, consonants, vowels):
    """__common_triplet(input_string, consonants, vowels) -> string"""
    output = consonants

    if len(input_string) > 2:
        # likely
        stopat = 3
    else:
        # unlikely (eg: surname = Fo)
        stopat = 2 

    while len(output) < stopat:
        output += vowels.pop(0)
    
    if len(output) == 2:
        output += 'X'

    return output[:3]

def __consonants_and_vowels(input_string):
    """__consonants_and_vowels(input_string) -> (string, list)

    Get the consonants as a string and the vowels as a list.
    """
    input_string = input_string.upper().replace(' ', '')

    consonants = [ char for char in input_string if char in __CONSONANTS ]
    vowels     = [ char for char in input_string if char in __VOWELS ]

    return "".join(consonants), vowels

def __surname_triplet(input_string):
    """__surname_triplet(input_string) -> string"""
    consonants, vowels = __consonants_and_vowels(input_string)

    return __common_triplet(input_string, consonants, vowels)

def __name_triplet(input_string):
    """__name_triplet(input_string) -> string"""
    if input_string == '':
        # highly unlikely: no first name, like for instance some Indian persons
        # with only one name on the passport
        # pylint: disable=W0511
        return 'XXX' 

    consonants, vowels = __consonants_and_vowels(input_string)
    
    if len(consonants) > 3:
        return "%s%s%s" % (consonants[0], consonants[2], consonants[3])

    return __common_triplet(input_string, consonants, vowels)

def control_code(input_string):
    """``control_code(input_string) -> int``

    Computes the control code for the given input_string string. The expected
    input_string is the first 15 characters of a fiscal code.

    eg: control_code('RCCMNL83S18D969') -> 'H'
    """
    assert len(input_string) == 15

    # building conversion tables for even and odd characters positions
    even_controlcode = {}

    for idx, char in enumerate(string.digits):
        even_controlcode[char] = idx

    for idx, char in enumerate(string.ascii_uppercase):
        even_controlcode[char] = idx

    values = [ 1, 0, 5, 7, 9, 13, 15, 17, 19, 21, 2, 4, 18, 20, 11, 3, 6, 8,
               12, 14, 16, 10, 22, 25, 24, 23 ]

    odd_controlcode = {}

    for idx, char in enumerate(string.digits):
        odd_controlcode[char] = values[idx]

    for idx, char in enumerate(string.ascii_uppercase):
        odd_controlcode[char] = values[idx]

    # computing the code
    code = 0
    for idx, char in enumerate(input_string):
        if idx % 2 == 0:
            code += odd_controlcode[char]
        else:
            code += even_controlcode[char]
    
    return string.ascii_uppercase[code % 26]

def build(surname, name, birthday, sex, municipality):
    """``build(surname, name, birthday, sex, municipality) -> string``

    Computes the fiscal code for the given person data.

    eg: build('Rocca', 'Emanuele', datetime.datetime(1983, 11, 18), 'M', 'D969') 
        -> RCCMNL83S18D969H
    """

    # RCCMNL
    output = __surname_triplet(surname) + __name_triplet(name)

    # RCCMNL83
    output += str(birthday.year)[2:]

    # RCCMNL83S
    output += MONTHSCODE[birthday.month - 1]

    # RCCMNL83S18
    output += "%02d" % (sex == 'M' and birthday.day or 40 + birthday.day)

    # RCCMNL83S18D969
    file = open(MUNICIPALITY_DB_PATH,'rU')
    for line in file:
        line_parsed_tuple = string.split(line,',')
        if(municipality.lower()==line_parsed_tuple[1]):
            output += municipality.upper()
        elif(municipality.lower()==line_parsed_tuple[0]):
            output += line_parsed_tuple[1].upper()
    #else
    if(not len(output)==15): raise Exception("municipality not found in the db")

    # RCCMNL83S18D969H
    output += control_code(output)

    assert isvalid(output)

    return output

# info from fiscal code 
def get_birthday(code):
    """``get_birthday(code) -> string``

    Birthday of the person whose fiscal code is 'code', in the format DD-MM-YY. 

    Unfortunately it's not possible to guess the four digit birth year, given
    that the Italian fiscal code uses only the last two digits (1983 -> 83).
    Therefore, this function returns a string and not a datetime object.

    eg: birthday('RCCMNL83S18D969H') -> 18-11-83
    """
    assert isvalid(code)

    day = int(code[9:11])
    day = day < 32 and day or day - 40

    month = MONTHSCODE.index(code[8]) + 1
    year = int(code[6:8])

    return "%02d-%02d-%02d" % (day, month, year)

def get_sex(code):
    """``get_sex(code) -> string``

    The sex of the person whose fiscal code is 'code'.

    eg: sex('RCCMNL83S18D969H') -> 'M'
        sex('CNTCHR83T41D969D') -> 'F'
    """
    
    assert isvalid(code)

    return int(code[9:11]) < 32 and 'M' or 'F'


def get_municipality(code):
    """``get_municipality(code) -> string``

    The municipality of the person whose fiscal code is 'code'.

    eg: ...
    """
    assert isvalid(code)
    
    subcode=code[11:15]
    subcode=subcode.lower()

    file = open(MUNICIPALITY_DB_PATH,'rU')
    for line in file:
        line_parsed_tuple = string.split(line,',')
        if(subcode==line_parsed_tuple[1]):
            return(line_parsed_tuple[0].capitalize()+" ("+line_parsed_tuple[2].rstrip().upper()+")")
    #else
    raise Exception("municipality not found in db")


# CLI interface for standalone use
import sys
import datetime
if __name__ == '__main__':

	if(len(sys.argv)==6):
		try:
			surname=sys.argv[1]
			name=sys.argv[2]
			birthday=sys.argv[3]
			sex=sys.argv[4]
			municipality=sys.argv[5]
			code = build(surname, name, datetime.datetime(int(birthday[0:4]),int(birthday[4:6]),int(birthday[6:8])), sex, municipality)
			print(code)
		except:
			print("codicefiscale error: "+sys.exc_info()[1].args[0])
			exit(1)
		exit(0)
	
	elif(len(sys.argv)==2):
		code=sys.argv[1]
		code = code.upper()
		# check if well-formed
		if not isvalid(code):
			print("codicefiscale: code is NOT valid")
			exit(1)
		# else
		print("codicefiscale: code is valid, trying to decode...")
		print("surname contains: " + code[0:3])
		# TODO: try to guess the name from a db
		print("name contains: " + code[3:6])
		# TODO: try to guess the name from a db
		print("birthday: " + get_birthday(code))
		print("sex: " + get_sex(code))
		print("municipality: " + get_municipality(code))
		exit(0)


	#else print usage
	print("usage: codicefiscale CODE|SURNAME NAME YYYYMMDD SEX MUNICIPALITY")
	exit(0)
