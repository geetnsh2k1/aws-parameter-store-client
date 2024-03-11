import os

import boto3
from botocore.exceptions import ParamValidationError

from src.config import Parameter, ParameterType, TierType, DataType, ParameterDetails
from src.constants.error_codes import ErrorCodes
from src.constants.error_messages import ErrorMessages
from src.exception import ClientException


class ParameterStoreService:
    _instance = None

    # key definition : example => dev/application/credentials/database/host
    KEY = "/{env}/{service_name}/{key_type}/{subtype}/{parameter_name}"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ParameterStoreService, cls).__new__(cls, *args, **kwargs)
            cls._instance.client = boto3.client('ssm')
        return cls._instance

    @staticmethod
    def _get_parameter_key(
            parameter: Parameter
    ) -> str:
        env: str = os.environ.get("env")

        values = {
            'env': env,
            'service_name': parameter.service_name,
            'key_type': parameter.key_type,
            'subtype': parameter.subtype,
            'parameter_name': parameter.parameter_name
        }

        return ParameterStoreService.KEY.format(
            **values
        )

    def create_parameter(
            self,
            parameter: Parameter,
            value: str,
            parameter_type: ParameterType,
            description: str,
            overwrite: bool = True,
            tier_type: TierType = TierType.STANDARD,
            data_type: DataType = DataType.TEXT
    ) -> None:
        parameter_key: str = ParameterStoreService._get_parameter_key(
            parameter=parameter
        )

        params = {
            'Name': parameter_key,
            'Description': description,
            'Value': value,
            'Type': parameter_type,
            'Overwrite': overwrite,
            'Tier': tier_type,
            'DataType': data_type
        }

        # Include KeyId only if parameter_type is SecureString
        if parameter_type.__eq__(ParameterType.SECURE_STRING):
            # TODO: Move section and name to constants file
            key_id: str = "key-idXXXXYYYYYZZZZZ"
            params['KeyId'] = key_id

        try:
            self.client.put_parameter(**params)
        except ParamValidationError as parameter_validation_error:
            raise ClientException(
                error_code=ErrorCodes.PARAMETER_VALIDATION_ERROR,
                error_message=ErrorMessages.PARAMETER_VALIDATION_ERROR.format(parameter.parameter_name),
                error=parameter_validation_error
            )
        except Exception as error:
            raise ClientException(
                error_code=ErrorCodes.AMAZON_CLIENT_ERROR,
                error_message=ErrorMessages.AMAZON_CLIENT_ERROR,
                error=error
            )

    @staticmethod
    def _get_parameter_details(parameter) -> ParameterDetails:
        return ParameterDetails(
            parameter_name=parameter['Name'].split('/')[-1],
            parameter_value=parameter['Value']
        )

    def get_parameter(
            self,
            parameter: Parameter
    ) -> ParameterDetails:
        parameter_key: str = ParameterStoreService._get_parameter_key(
            parameter=parameter
        )

        try:
            response = self.client.get_parameter(
                Name=parameter_key,
                WithDecryption=True
            )
            return ParameterStoreService._get_parameter_details(parameter=response['Parameter'])
        except Exception as error:
            raise ClientException(
                error_code=ErrorCodes.AMAZON_CLIENT_ERROR,
                error_message=ErrorMessages.AMAZON_CLIENT_ERROR,
                error=error
            )

    def get_parameters(
            self,
            parameters: list[Parameter]
    ) -> list[ParameterDetails]:
        parameter_keys: list[str] = [
            ParameterStoreService._get_parameter_key(
                parameter=parameter
            )
            for parameter in parameters
        ]

        try:
            response = self.client.get_parameters(
                Names=parameter_keys,
                WithDecryption=True
            )
            return [
                ParameterStoreService._get_parameter_details(parameter=parameter)
                for parameter in response['Parameters']
            ]
        except Exception as error:
            raise ClientException(
                error_code=ErrorCodes.AMAZON_CLIENT_ERROR,
                error_message=ErrorMessages.AMAZON_CLIENT_ERROR,
                error=error
            )

    def delete_parameter(
            self,
            parameter: Parameter
    ) -> str:
        parameter_key: str = ParameterStoreService._get_parameter_key(
            parameter=parameter
        )

        try:
            self.client.delete_parameter(
                Name=parameter_key,
            )
            return parameter.parameter_name
        except Exception as error:
            raise ClientException(
                error_code=ErrorCodes.AMAZON_CLIENT_ERROR,
                error_message=ErrorMessages.AMAZON_CLIENT_ERROR,
                error=error
            )
