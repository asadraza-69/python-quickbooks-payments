from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.operations.tokenoperations import OperationsConverter


class Token:
    def __init__(self, data=None):
        self.value = None

        if data is not None:
            for name, value in data.items():
                if hasattr(self, name):
                    if value is not None:
                        if isinstance(value, dict):
                            class_name = getattr(ModulesConstants,
                                                 'NAMESPACE_MODULES') + OperationsConverter.to_upper_case_class_name(
                                name)
                            obj = globals()[class_name](value)
                            setattr(self, name, obj)
                        else:
                            setattr(self, name, value)

# Example Usage:
# data = {
#     "value": "token_value"
# }
# token = Token(data)
