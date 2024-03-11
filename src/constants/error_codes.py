from enum import Enum


class ErrorCodes(int, Enum):
    AMAZON_CLIENT_ERROR = 1000

    PARAMETER_VALIDATION_ERROR = 1001
    GET_PARAMETER_NOT_ALLOWED = 1002
