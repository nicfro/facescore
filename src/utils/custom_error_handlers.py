from fastapi import HTTPException, status


class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DBError(Exception):
    def __init__(self, message):
        super().__init__(message)


class AuthError(Exception):
    def __init__(self, message):
        super().__init__(message)


def forbidden_exception(reason):
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"{reason}",
        headers={"WWW-Authenticate": "Bearer"},
    )
