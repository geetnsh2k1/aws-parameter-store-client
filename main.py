from src.client import ParameterStoreService
from src.config import Parameter, KeyType

if __name__ == '__main__':
    # / local / application / configuration / loan_journey / forms_data
    print(
        ParameterStoreService().get_parameter(
            parameter=Parameter(
                parameter_name="forms_data",
                key_type=KeyType.CONFIGURATION,
                subtype="loan_journey"
            )
        )
    )
