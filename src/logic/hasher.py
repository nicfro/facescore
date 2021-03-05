from passlib.context import CryptContext
import random


class Hasher:
    def __init__(self):
        self.SALT_ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"], default="sha256_crypt")

    def verify(self, password, salt, hashed_password) -> bool:
        """Verify a password, given the salt and hash value of said pass word"""
        return self.myctx.verify(password+salt, hashed_password)

    def hash(self, password) -> (str, str):
        """Hash a password with a generated salt"""
        salt=[]
        [salt.append(random.choice(self.SALT_ALPHABET)) for x in range(16)]
        salt = "".join(salt)
        hash_value = self.myctx.hash(password+salt)
        return hash_value, salt

