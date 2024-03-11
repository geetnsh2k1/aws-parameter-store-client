from typing import Union, Any


class ClientException(Exception):
    def __init__(self, error_code: int, error_message: str, error: Union[Any, None] = None, status_code: int = 500):
        super().__init__(error_code, error_message, error, status_code)
