import os
import sys

sys.path.insert(0, os.getcwd())

import unittest
from src.logic.shared_logic.hasher import Hasher
from src.utils.common_logger import logger


class TestHasher(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHasher, self).__init__(*args, **kwargs)
        self.HASH = Hasher()

    def test_01_hashing(self):
        password = "123456"
        hashed_password, salt = self.HASH.hash(password)
        result = self.HASH.verify(password, salt, hashed_password)
        self.assertTrue(result)
