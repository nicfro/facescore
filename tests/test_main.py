import os
import sys

sys.path.insert(0, os.getcwd())

import unittest
import tests.logic.test_hasher as test_hasher
import tests.logic.test_elo as test_elo


suite = unittest.TestLoader().loadTestsFromModule(test_hasher)
suite1 = unittest.TestLoader().loadTestsFromModule(test_elo)

unittest.TextTestRunner(verbosity=2).run(suite)
unittest.TextTestRunner(verbosity=2).run(suite1)