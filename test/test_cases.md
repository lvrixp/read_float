#Test#

## Test Enumeration ##

Following test cases are for testing `count_and_sum` function.

### Positive test cases ###

1.Normal  

    Input :  ["1.23 0 0", "22 -4.2", "0"]
    Expected : (6, 19.03)

2.Input file contains only one number

    Input: ["1.01"]
    Expected: (1, 1.01)

3.Input file contains continuous spaces

    Input: ["   -1.0", "   1.1 2.2", "3.3 4.4    ", "  -5.5   ", "    "]
    Expected: (6, 4.5)

4.Input file contains tab

    Input: ["\t1.0", "\t1.1 2.2", "3.3 4.4\t ", " \t 5.5 \t  ", " \t   "]
    Expected: (6, 17.5)
    
5.Empty file

    Input: []
    Expected: (0,  0)

6.Input file contains only empty lines

    case=["","",""]
    Expected: (0,0)

7.Some lines in the input file are empty

    case=["","","", "22.00 23", "", "1", ""]
    Expected: (3, 46)
    
8.Input file contains only spaces.

    case=[" ", " ", "   "]
    Expected: (0, 0)

9.Each line contains only one number

    Input: ["1", "101", "1"]
    Expected: (3, 103) 

**10.Test precision(self):**

    Input: ["0.99999999999999999999999999999"]
    #TODO : What's the output. 1 or 0.99999999999999999999999999999
    Expected: (1, 1)
    Expected:    (1, 0.99999999999999999)
    self.assertNotEqual(count_and_sum(case), (1, 0.9999999999999999)
    
 11.Floats in kinds of format

    Input: [".01"]
    Expected: (1, 0.01)

    Input: ["-.01"]
    Expected: (1, -0.01)
    
    Input: ["01"]
    Expected: (1, 1)

    Input: ["-001"]
    Expected: (1, -1)

    Input: ["+001"]
    Expected: (1, 1)

    Input: ["10,000.00"]
    #TODO: bug?
    #Expected: (1, 10000)

    Input: ["-10,010,000.00"]
    #TODO: bug?
    #Expected: (1, -10010000)
    
12.Large float or special float
    
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
    
    Input: [smallPrecisionFloat,"0"]
    Expected: (2, 2.2250738585072014E-400)
    
    Input: [largePrecisionFloat, "0" ]
    Expected: (2, 1.7976931348623158E+400)

    Input: [smallPrecisionFloat, largePrecisionFloat]
    Expected: (2, float('inf'))

    Input: [smallPrecisionFloat, "0", largePrecisionFloat]
    Expected: (3, float('inf'))

    Input: ["0", minFloat]
    Expected: (2, -1.7976931348623158E+308)

    Input: ["0", smallerThanMinFloat]
    Expected: (2, float('-inf'))

    Input: [infFloat, "0"]
    Expected: (2, float('inf'))

    Input: [negInfFloat, "0"]
    Expected: (2, float('-inf'))

    Input: [infFloat, negInfFloat]
    #TODO : Do not know how to compare.
    #Expected: (2, float('Nan'))

    Input: [nanFloat, "0"]
    #Expected: (2, float('nan'))

    Input: [upperNanFloat, negNanFloat, "0"]
    #Expected: (3, float('nan'))
    
    
13.File contains other characters

    Contains dot:

	    Input: ["1 . 1", "1.1"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (3, 3.1)

    Contains % /
   
	    Input: ["1%1", "1/4"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)

    Contains E and sign
	    Input: ["1.175494351 E - 38"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (2, 39.175494351)

    Contains sign
	    Input: ["5-5"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
	
	    Input: ["++001"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
	    
	    Input: ["-+001"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)

    Contains suffix which is in valid in other languages

	    Input: ["1d"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
	
	    Input: ["1f"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
	
	    Input: ["1L"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
	
	    Input: ["1m"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
    
    Contains other letters or charactors     
    
	    Input: ["aaa", "bb", "cc "]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (0, 0)
	
	    Input: ["1.2", "abc 3.2 323d2"]
	    expected: (ValueError)
	    #self.assertEqual(count_and_sum(case, true), (2, 4.4)
    
14.File in large size

15.File contains a very long line
