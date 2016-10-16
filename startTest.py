'''
Created on 2016.10.16

@author: chen
'''

import unittest
import doctest
from code import tedUtils
    

if __name__ == '__main__':
    suite = doctest.DocTestSuite()
    suite.addTests(doctest.DocTestSuite(tedUtils))
    unittest.TextTestRunner(verbosity=2).run(suite)
