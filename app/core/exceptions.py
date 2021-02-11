
class AppException(Exception):
    pass


class ArgsError(AppException):
    pass


class AppiumNotFound(AppException):
    pass


class AppiumNotStart(AppException):
    pass


class NotImplementedError(AppException):
    pass
