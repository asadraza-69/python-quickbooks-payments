from .modulesconstants import ModulesConstants
from ..operations import OperationsConverter


class ZeroDollarVerification:
    def __init__(self, data=None):
        self.status = None
        self.type = None
        self.transaction_id = None

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
#     "status": "approved",
#     "type": "verification",
#     "transaction_id": "tx12345"
# }
# zero_dollar_verification = ZeroDollarVerification(data)
