import os
import sys

sys.path.insert(0, os.getcwd())

import unittest
from src.logic.shared_logic.user import UserCreator
from src.utils.common_logger import logger


class TestUser(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestUser, self).__init__(*args, **kwargs)
        self.user = UserCreator()

    def test_01_create_user(self):
        password = "123456"
        hashed_password, salt = self.HASH.hash(password)
        result = self.HASH.verify(password, salt, hashed_password)
        self.assertTrue(result)
