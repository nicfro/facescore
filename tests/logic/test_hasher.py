import os
from sre_compile import isstring
import sys

sys.path.insert(0, os.getcwd())

import unittest

from src.logic.hasher import Hasher

class TestHasher(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHasher, self).__init__(*args, **kwargs)
        self.hasher = Hasher()

    def test_01_user_hash_and_salt_is_different(self):
        pw1, salt1 = self.hasher.user_hash("123")
        pw2, salt2 = self.hasher.user_hash("123")
        self.assertFalse(pw1 == pw2)
        self.assertFalse(salt1 == salt2)

    def test_02_can_create_and_verify_password(self):
        password = "hehexd"
        hashed_password, salt = self.hasher.user_hash(password)
        self.assertTrue(self.hasher.verify("hehexd", salt, hashed_password))

    def test_03_can_hash_image_file(self):
        image = b"hehehehehehehehheheheh"
        res = self.hasher.image_hash(image)
        self.assertTrue(isstring(res))