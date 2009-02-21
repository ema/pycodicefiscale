
import unittest

import datetime
from codicefiscale import isvalid, get_birthday, get_sex, control_code, build

class TestRepos(unittest.TestCase):
    
    def test_isvalid(self):
        invalid = [ None, True, 16, "RCCMNL", 
                    # the first 'I' shouldn't be there
                    "CSTNGL22I10D086I" ]

        for cf in invalid:
            self.assertFalse(isvalid(invalid))

    def test_get_birthday(self):
        inputs = { 
            'MRTNTN23M02D969P': '2-8-23',
            'RCCMNL83S18D969H': '18-11-83',
            'MRSMSR81D60Z611H': '20-4-81',
            'CNTCHR83T41D969D': '1-12-83'
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
        }
                     
        for cf, expected in inputs.items():
            self.assertEquals(expected, get_sex(cf))

    def test_control_code(self):
        inputs = { 
            'MRTNTN23M02D969': 'P',
            'MRSMSR81D60Z611': 'H',
            'RCDLSN84S16D969': 'Z',
            'CNTCHR83T41D969': 'D',
            'BNCSFN85T58G702': 'W',
            'RCCMNL83S18D969': 'H',
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
            )
        }
        
        for expected, data in tests.items():
            cf = build(surname=data[0], name=data[1], 
                       birthday=data[2], sex=data[3],
                       municipality=data[4])
        
            self.assertEquals(expected, cf)

if __name__ == "__main__":
    unittest.main()
