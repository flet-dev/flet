class FletException(Exception):
    pass


class FletUnsupportedPlatformException(FletException):
    """
    Thrown by operations that are not supported on the current platform.
    """

    def __init__(self, message: str):
        super().__init__(message)


class FletUnimplementedPlatformEception(FletUnsupportedPlatformException):
    """
    Thrown by operations that have not been implemented yet.
    """

    pass
