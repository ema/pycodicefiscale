from __future__ import print_function

import unittest

import datetime
import locale

from codicefiscale import isvalid, get_birthday, get_sex, control_code, build

class TestRepos(unittest.TestCase):
    
    def test_isvalid(self):
        invalid = [ None, True, 16, "RCCMNL", 
                    # the first 'I' shouldn't be there
                    "CSTNGL22I10D086I" ]

        for cf in invalid:
            self.assertFalse(isvalid(cf))
        
        valid = ( 'MRTNTN23M02D969P', 
                  'RCCMNL83S18D969H', 
                  'MRSMSR81D60Z611H',
                  'CNTCHR83T41D969D', 
                  'FOXDRA26C24H872Y',
                  'MAILCU91A25F839D',
                  'RSSMRA45C12F205C',
                  'RSSMRA45C12F20RX',
                  'RSSMRA45C12F2L5N',
                  'RSSMRA45C12F2LRI',
                  'RSSMRAQRCMNFNLRG',)

        for cf in valid:
            self.assertTrue(isvalid(cf))

    def test_get_birthday(self):
        inputs = { 
            'MRTNTN23M02D969P': '02-08-23',
            'RCCMNL83S18D969H': '18-11-83',
            'MRSMSR81D60Z611H': '20-04-81',
            'CNTCHR83T41D969D': '01-12-83',
            'FOXDRA26C24H872Y': '24-03-26',
            'MAILCU91A25F839D': '25-01-91',
            'RSSMRA45C12F205C': '12-03-45',
            'RSSMRA45C12F20RX': '12-03-45',
            'RSSMRA45C12F2L5N': '12-03-45',
            'RSSMRA45C12F2LRI': '12-03-45',
            'RSSMRAQRCMNFNLRG': '12-03-45',
        }
                     
        for cf, expected in inputs.items():
            self.assertEquals(expected, get_birthday(cf))

    def test_get_sex(self):
        inputs = { 
            'MRTNTN23M02D969P': 'M',
            'RCCMNL83S18D969H': 'M',
            'RCDLSN84S16D969Z': 'M',
            'MRSMSR81D60Z611H': 'F',
            'CNTCHR83T41D969D': 'F',
            'FOXDRA26C24H872Y': 'M',
            'MAILCU91A25F839D': 'M'
        }
                     
        for cf, expected in inputs.items():
            self.assertEquals(expected, get_sex(cf))

    def test_control_code(self):
        inputs = { 
            # fiscal codes tested in this module
            'MRTNTN23M02D969': 'P',
            'MRSMSR81D60Z611': 'H',
            'RCDLSN84S16D969': 'Z',
            'CNTCHR83T41D969': 'D',
            'BNCSFN85T58G702': 'W',
            'RCCMNL83S18D969': 'H',
            'FOXDRA26C24H872': 'Y',
            'MAILCU91A25F839': 'D'
        }

        for cf, expected in inputs.items():
            self.assertEquals(expected, control_code(cf))

    def test_build(self):
        tests = { 

            'RCCMNL83S18D969H': ( 
                "Rocca", "Emanuele", 
                datetime.datetime(1983, 11, 18),
                'M','D969'
            ),

            'CNTCHR83T41D969D': ( 
                "Cintoi", "Chiara", 
                datetime.datetime(1983, 12, 1),
                'F','D969'
            ),

            'BNCSFN85T58G702W': ( 
                "Bianucci", "Stefania", 
                datetime.datetime(1985, 12, 18),
                'F','G702'
            ),

            'RCDLSN84S16D969Z': ( 
                "Arcidiacono", "Alessandro", 
                datetime.datetime(1984, 11, 16),
                'M','D969'
            ),

            'FOXDRA26C24H872Y': ( 
                "Fo", "Dario", 
                datetime.datetime(1926, 3, 24),
                'M',
                # born in Sangiano
                'H872'
            ),

            'MAILCU91A25F839D': (
                "Maio", "Luca",
                datetime.datetime(1991, 1, 25),
                'M',
                'F839'
            ),

            'HRYXXX11S05Z222K': (
                "Haryana", 
                # Indian person with only one name reported on her passport
                "",
                datetime.datetime(1911, 11, 5),
                'M',
                'Z222'
            ),

            'FOXMRA83S18D969V': (
                "Fo'", "Mario",
                # Short surname with apostrophe
                datetime.datetime(1983, 11, 18),
                'M','D969'
            ),

            'YXXAXX83S18D969R': (
                "Y", "A",
                # Extremely short surname, and name (Korean example)
                datetime.datetime(1983, 11, 18),
                'M','D969'
            ),

        }
        
        for expected, data in tests.items():
            cf = build(surname=data[0], name=data[1], 
                       birthday=data[2], sex=data[3],
                       municipality=data[4])
        
            self.assertEquals(expected, cf)

class TestBugs(unittest.TestCase):

    def test_01_locale_bug(self):
        try:
            locale.setlocale(locale.LC_ALL, "it_IT")
        except locale.Error:
            print("Skipping test_01_locale_bug, it_IT not available")
            return

        expected = "MRARSS91A25G693C"
        actual = build("mario", "rossi", datetime.datetime(1991, 1, 25), "M", "G693")
        self.assertEquals(expected, actual)

    def test_02_get_birthday_format(self):
        self.assertEquals('02-08-23', get_birthday('MRTNTN23M02D969P'))

    def test_03_unicode_handling_isvalid(self):
        self.assertTrue(isvalid('MRTNTN23M02D969P'))
        self.assertTrue(isvalid(u'MRTNTN23M02D969P'))

if __name__ == "__main__":
    unittest.main()
