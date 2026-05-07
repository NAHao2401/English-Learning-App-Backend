class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "APP_ERROR"
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="NOT_FOUND"
        )


class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(
            message=message,
            status_code=400,
            error_code="BAD_REQUEST"
        )


class TooManyRequestsException(AppException):
    def __init__(self, message: str = "Too many requests"):
        super().__init__(
            message=message,
            status_code=429,
            error_code="TOO_MANY_REQUESTS"
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="FORBIDDEN"
        )