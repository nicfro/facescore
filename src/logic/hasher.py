import hashlib
import random


class Hasher:
    def __init__(self):
        self.SALT_ALPHABET = (
            "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

        self.hasher = hashlib.new("sha256")

    def verify(self, password: str, salt: str, hashed_password: str) -> bool:
        """Verify a password, given the salt and hash value of said password"""
        self.hasher.update(password.encode())
        self.hasher.update(salt.encode())
        result = self.hasher.hexdigest()

        self.hasher = hashlib.new("sha256")
        return result == hashed_password

    def user_hash(self, password: str):
        """Hash a password with a generated salt"""
        salt = []
        [salt.append(random.choice(self.SALT_ALPHABET)) for x in range(16)]
        salt = "".join(salt)

        self.hasher.update(password.encode())
        self.hasher.update(salt.encode())
        result = self.hasher.hexdigest()

        self.hasher = hashlib.new("sha256")
        return result, salt

    def image_hash(self, image: str):
        """Hash a base64 encoded image"""
        self.hasher.update(image.encode("utf-8"))
        result = self.hasher.hexdigest()

        self.hasher = hashlib.new("sha256")
        return result
