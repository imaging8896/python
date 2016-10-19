'''
Created on 2016.10.16

@author: chen
'''

import unittest
import doctest
from code.aliasUtils import aliasUtils


if __name__ == '__main__':
    aliasUtils.setup()

    suite = doctest.DocTestSuite()
    suite.addTests(doctest.DocTestSuite(aliasUtils))
    unittest.TextTestRunner(verbosity=2).run(suite)

    aliasUtils.cleanup()
