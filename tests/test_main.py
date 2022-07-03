import os
import sys

sys.path.insert(0, os.getcwd())

import unittest
import tests.logic.test_hasher as test_hasher

suite = unittest.TestLoader().loadTestsFromModule(test_hasher)
unittest.TextTestRunner(verbosity=2).run(suite)