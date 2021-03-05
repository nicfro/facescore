import os
import sys
import time
sys.path.insert(0, os.getcwd())

import unittest
from src.logic.shared_logic.jwt_handler import *
from src.utils.common_logger import logger


class TestJwt(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestJwt, self).__init__(*args, **kwargs)

    def test_01_create_auth_token(self):
        test_user_id = "test_user_id"
        test_duration = 94871

        token = encode_auth_token(test_user_id, test_duration)
        print(type(token))
        self.assertTrue(isinstance(token,str))

    def test_02_deode_valid_auth_token(self):
        test_user_id = "test_user"
        test_duration = 1000

        token = encode_auth_token(test_user_id, test_duration)
        decoded = decode_auth_token(token)

        self.assertTrue(isinstance(decoded, int))

    def test_03_decode_invalid_auth_token(self):
        test_user_id = "test_user"
        test_duration = 0

        token = encode_auth_token(test_user_id, test_duration)
        decoded = decode_auth_token(token)

        self.assertTrue(isinstance(decoded, str))

    def test_04_expired_auth_token(self):
        test_user_id = "test_user"
        test_duration = 1

        token = encode_auth_token(test_user_id, test_duration)
        decoded_valid = decode_auth_token(token)

        time.sleep(1.5)

        decoded_invalid = decode_auth_token(token)

        self.assertTrue(isinstance(decoded_valid, int))
        self.assertTrue(isinstance(decoded_invalid, str))
