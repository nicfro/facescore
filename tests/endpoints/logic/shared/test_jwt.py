import os
import sys
import time
sys.path.insert(0, os.getcwd())

import unittest
from src.logic.jwt_handler import encode_auth_token, decode_auth_token
from src.utils.common_logger import logger


class TestJwt(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestJwt, self).__init__(*args, **kwargs)

    def test_01_create_auth_token(self):
        test_user_id = "test_user_id"
        test_duration = 94871

        token = encode_auth_token(test_user_id, test_duration)
        self.assertTrue(isinstance(token,str))

    def test_02_deode_valid_auth_token(self):
        test_user_id = "test_user"
        test_duration = 100000

        token = encode_auth_token(test_user_id, test_duration)
        decoded = decode_auth_token(token)

        self.assertTrue(decoded == test_user_id)

    def test_03_decode_expired_auth_token(self):
        test_user_id = "test_user"
        test_duration = 0.5

        token = encode_auth_token(test_user_id, test_duration)
        time.sleep(2)
        decoded = decode_auth_token(token)


        self.assertTrue(decoded == "Signature expired. Please log in again.")

    def test_04_decode_invalid_auth_token(self):
        decoded = decode_auth_token("totallywrongtoken")
        self.assertTrue(decoded == "Invalid token. Please log in again.")