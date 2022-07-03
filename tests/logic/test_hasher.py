import os
import sys

sys.path.insert(0, os.getcwd())

import unittest

from src.logic.hasher import Hasher

class TestHasher(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHasher, self).__init__(*args, **kwargs)
        self.hasher = Hasher()

    def test_01_user_hash_is_same_salt_is_different(self):
        pw1, salt1 = Hasher.user_hash("123")
        pw2, salt2 = Hasher.user_hash("123")
        self.assertTrue(pw1 == pw2)
        self.assertFalse(salt1 == salt2)


