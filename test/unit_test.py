#!/usr/bin/python
'''Unit test for the tool read_float

This unit test focus on the core function
in the tool which is count and sum

TODO:
    Tool functional test on various files
'''

import sys
import os
import unittest

BASEDIR = os.path.dirname(sys.argv[0])
SRCDIR = os.path.join(BASEDIR, '../src')
sys.path.insert(0, SRCDIR)

from read_float import count_and_sum

class TestCountAndSum(unittest.TestCase):
    def test_normal(self):
        #case = ["1.23 0 0", "22 -4.2", "0"]
        case = "1.23 0 0 22 \n-4.2 0"
        self.assertEqual(count_and_sum(case), (6, 19.03))
        
    def test_onlyOneFloat(self):
        case = "1.01"
        self.assertEqual(count_and_sum(case), (1, 1.01))

    def test_precision(self):
        case = "0.99999999999999999999999999999"
        self.assertEqual(count_and_sum(case), (1, 1))
        self.assertEqual(count_and_sum(case),    (1, 0.99999999999999999))
        self.assertNotEqual(count_and_sum(case), (1, 0.9999999999999999))
        
    def test_specialFormat(self):
        case = ".01"
        self.assertEqual(count_and_sum(case), (1, 0.01))

        case = "-.01"
        self.assertEqual(count_and_sum(case), (1, -0.01))
        
        case = "01"
        self.assertEqual(count_and_sum(case), (1, 1))

        case = "-001"
        self.assertEqual(count_and_sum(case), (1, -1))

        case = "+001"
        self.assertEqual(count_and_sum(case), (1, 1))

        case = "25%"
        self.assertRaises(ValueError, count_and_sum, case, )

        case = "10,000.00"

        #we used locale to parse it, so it won't raise exception
        #self.assertRaises(ValueError, count_and_sum, case, )

        self.assertEqual(count_and_sum(case), (1, 10000))

        case = "-10,010,000.00"
        self.assertEqual(count_and_sum(case), (1, -10010000))
        
    # Large number or special number
    def test_SpecialNumber(self):
        smallPrecisionFloat = "2.2250738585072014E-400"
        largePrecisionFloat = "1.7976931348623158e+400"
        minFloat = "-1.7976931348623158E+308"
        smallerThanMinFloat = "-1.7976931348623158E+309"
        infFloat = "inf"
        upperInfFloat = "INF"
        negInfFloat = "-inf"
        upperNegInfFloat = "-Inf"
        nanFloat = "nan"
        upperNanFloat = "NaN"
        negNanFloat = "-Nan"
        case = smallPrecisionFloat + " 0"
        self.assertEqual(count_and_sum(case), (2, 2.2250738585072014E-400))
        case = largePrecisionFloat + " 0" 
        self.assertEqual(count_and_sum(case), (2, 1.7976931348623158E+400))
        case = smallPrecisionFloat + ' ' + largePrecisionFloat
        self.assertEqual(count_and_sum(case), (2, float('inf')))
        case = smallPrecisionFloat + " 0 " + largePrecisionFloat
        self.assertEqual(count_and_sum(case), (3, float('inf')))
        case = "0 " + minFloat
        self.assertEqual(count_and_sum(case), (2, -1.7976931348623158E+308))
        case = "0 " + smallerThanMinFloat
        self.assertEqual(count_and_sum(case), (2, float('-inf')))
        case = infFloat + " 0"
        self.assertEqual(count_and_sum(case), (2, float('inf')))
        case = negInfFloat + " 0"
        self.assertEqual(count_and_sum(case), (2, float('-inf')))
        case = infFloat + ' ' + negInfFloat
        #TODO : Do not know how to compare.
        #self.assertEqual(count_and_sum(case), (2, float('Nan')))
        case = [nanFloat, "0"]
        #self.assertEqual(count_and_sum(case), (2, float('nan')))
        case = [upperNanFloat, negNanFloat, "0"]
        #self.assertEqual(count_and_sum(case), (3, float('nan')))
        
    # Line parse #
    def test_ContinuesSpaces(self):
        case = "   -1.0    1.1 2.2 3.3 4.4      -5.5       "
        self.assertEqual(count_and_sum(case), (6, 4.5))

    def test_Tab(self):    
        case = "\t1.0 1.1 2.2 3.3 4.4\t  \t 5.5 \t   \t   "
        self.assertEqual(count_and_sum(case), (6, 17.5))
        
    # Special charactor
    def test_dot(self):
        case = "1 . 1 1.1"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (3, 3.1))

        case = "1.175494351 E - 38"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (2, 39.175494351))

        case = "5-5"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))

        case = "++001"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))
        
        case = "-+001"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))

        case = "1d"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))

        case = "1f"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))

        case = "1L"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))

        case = "1m"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))
        
    # Special file
    def test_emptyFile1(self):
        case = ""
        self.assertEqual(count_and_sum(case), (0,  0))

    def test_fileWithEmptyLines(self):
        case="\n\n\n"
        self.assertEqual(count_and_sum(case), (0,0))

    def test_eachLineContainsOnlyOneFloat(self):
        case = "1\n101\n1"
        self.assertEqual(count_and_sum(case), (3, 103))
                
    def test_fileWithOtherCharaters(self):
        case="aaa\nbb\ncc "
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (0, 0))

    def test_ValueErrorl(self):
        case = "1.2\nabc\n 3.2 323d2"
        self.assertRaises(ValueError, count_and_sum, case, )
        #self.assertEqual(count_and_sum(case, true), (2, 4.4))
        

if __name__ == '__main__':
    unittest.main()
