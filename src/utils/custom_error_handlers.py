class ConfigError(Exception):
    def __init__(self, message):
        super().__init__(message)


class DBError(Exception):
    def __init__(self, message):
        super().__init__(message)
