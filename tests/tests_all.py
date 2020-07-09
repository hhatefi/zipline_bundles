import unittest

import csv_ingester_test
import direct_ingester_test

loader=unittest.TestLoader()
suite=unittest.TestSuite()

suite.addTest(loader.loadTestsFromModule(csv_ingester_test))
suite.addTest(loader.loadTestsFromModule(direct_ingester_test))

runner=unittest.TextTestRunner(verbosity=3)
result=runner.run(suite)
