from enum import Enum


class ErrorMessages(str, Enum):
    AMAZON_CLIENT_ERROR = "An error occurred while interacting with AWS, Please try again later. "

    PARAMETER_VALIDATION_ERROR = "Parameter: {}, is not a valid parameter to store at ssm parameter store."
    GET_PARAMETER_NOT_ALLOWED = "Parameter: {}, is not allowed to be fetched since it is not an application parameter."
