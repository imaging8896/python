'''
Created on 2016.10.16

@author: chen
'''

import unittest
import doctest
from code.hcfsUtils import hcfsUtils


if __name__ == '__main__':
    hcfsUtils.setup()

    suite = doctest.DocTestSuite()
    suite.addTests(doctest.DocTestSuite(hcfsUtils))
    unittest.TextTestRunner(verbosity=2).run(suite)

    hcfsUtils.cleanup()
