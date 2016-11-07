'''
Created on 2016.10.16

@author: chen
'''

import unittest
import doctest
from code.mgmtAppUtils import mgmtAppUtils


if __name__ == '__main__':
    mgmtAppUtils.setup()

    suite = doctest.DocTestSuite()
    suite.addTests(doctest.DocTestSuite(mgmtAppUtils))
    unittest.TextTestRunner(verbosity=2).run(suite)

    mgmtAppUtils.cleanup()
