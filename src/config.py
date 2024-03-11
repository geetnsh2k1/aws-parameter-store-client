from enum import Enum

from pydantic import BaseModel, Field


class ParameterType(str, Enum):
    STRING = "String"
    STRING_LIST = "StringList"
    SECURE_STRING = "SecureString"


class TierType(str, Enum):
    STANDARD = "Standard"
    ADVANCED = "Advanced"


class DataType(str, Enum):
    TEXT = "text"
    AMAZON_MACHINE_ID = "aws:ec2:image"


class ServiceType(str, Enum):
    # we can list as many as per our requirements
    APPLICATION = "application"  # this is used across all the services
    LAMBDA = "lambda"
    AMAZON_SES = "ses"  # amazon simple email service
    AMAZON_S3 = "s3"


class KeyType(str, Enum):
    CONFIGURATION = "configuration"
    CREDENTIALS = "credentials"
    CONSTANTS = "constants"


class Parameter(BaseModel):
    parameter_name: str
    key_type: KeyType
    subtype: str
    service_name: ServiceType = Field(default=ServiceType.APPLICATION)


class ParameterDetails(BaseModel):
    parameter_name: str
    parameter_value: str
