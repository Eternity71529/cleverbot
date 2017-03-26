class CleverConfigurationError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error

class CleverAPIError(Exception):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        return self.error
