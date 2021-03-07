import jwt
import datetime
import os
import time

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

def encode_auth_token(user_id, duration):
    """
    Generates the Auth Token
    :return: string
    """
    #convert duration into days, hours, minutes, seconds
    days, hours, minutes, seconds = duration_to_timedelta(duration)
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            "KEY",
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, "KEY", algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'


def decode_auth_token_decorator(auth_token):
    """
    Decodes the auth token before the function is called.
    """
    def decorator(func):
        def wrapped_func(*args, **kwargs):
            decode_auth_token(auth_token)
            return func(*args, **kwargs)
        return wrapped_func
    return decorator
