'''
Created on 2016.10.16

@author: chen
'''

import unittest
import doctest
from code.aliasUtils import aliasUtils
from code.hcfsUtils import hcfsUtils
from code.mgmtAppUtils import mgmtAppUtils


if __name__ == '__main__':
    aliasUtils.setup()
    hcfsUtils.setup()
    mgmtAppUtils.setup()

    suite = doctest.DocTestSuite()
    suite.addTests(doctest.DocTestSuite(aliasUtils))
    suite.addTests(doctest.DocTestSuite(hcfsUtils))
    suite.addTests(doctest.DocTestSuite(mgmtAppUtils))
    unittest.TextTestRunner(verbosity=2).run(suite)

    aliasUtils.cleanup()
    hcfsUtils.cleanup()
    mgmtAppUtils.cleanup()
