import os
import sys
sys.path.insert(0, os.getcwd())


import jwt
import datetime
from fastapi import Depends

from src.settings import load_config
from src.utils.common_logger import logger
from src.utils.custom_error_handlers import ConfigError
from src.logic.auth import OAuth2PasswordBearerCookie

oauth2_scheme = OAuth2PasswordBearerCookie(tokenUrl="/token")

class JWT_Handler:
    def __init__(self):
        # Load parameters from .ENV
        if os.path.isfile('ENV'):
            load_config('ENV')

        self.JWT_KEY = os.environ.get('JWT_KEY')

        # Check required fields exist
        if None in [os.environ.get('JWT_KEY')]:
            logger.error("Could not retrieve JWT Key")
            raise ConfigError("Could not retrieve JWT Key")

    @staticmethod
    def duration_to_timedelta(duration):
        """
        Compute duration (in seconds) to days, hours, minutes, and seconds.
        """
        # Compute days
        secs_per_day = 24*60*60
        days = duration // secs_per_day
        rem_duration = duration - days * secs_per_day

        # Compute hours
        secs_per_hour = 60*60
        hours = rem_duration // secs_per_hour
        rem_duration -= hours * secs_per_hour
        
        # Compute minutes
        secs_per_minute = 60
        minutes = rem_duration // secs_per_minute
        rem_duration -= minutes * secs_per_minute
        
        # Compute seconds (remaining)
        seconds = rem_duration

        return days, hours, minutes, seconds


    async def decode_auth_token(self, auth_token: str = Depends(oauth2_scheme)):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, self.JWT_KEY, algorithms=["HS256"])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def encode_auth_token(self, user_id, duration):
        """
        Generates the Auth Token
        :return: string
        """
        #convert duration into days, hours, minutes, seconds
        days, hours, minutes, seconds = self.duration_to_timedelta(duration)
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                self.JWT_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e