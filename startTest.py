'''
Created on 2016.10.16

@author: chen
'''

import unittest
import doctest
from code.tedUtils import tedUtils, osUtils
from code import FuncSpec


if __name__ == '__main__':
    suite = doctest.DocTestSuite()
    suite.addTests(doctest.DocTestSuite(tedUtils))
    suite.addTests(doctest.DocTestSuite(osUtils))
    suite.addTests(doctest.DocTestSuite(FuncSpec))
    unittest.TextTestRunner(verbosity=2).run(suite)
