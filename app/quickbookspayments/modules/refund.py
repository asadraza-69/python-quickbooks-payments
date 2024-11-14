from .modulesconstants import ModulesConstants
from ..operations import OperationsConverter


class Refund:
    def __init__(self, data=None):
        self.id = None
        self.created = None
        self.status = None
        self.amount = None
        self.context = None
        self.description = None
        self.type = None

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
#     "id": "refund123",
#     "created": "2021-01-01",
#     "status": "completed",
#     "amount": 50.0,
#     "context": {"device_info": "device123"},
#     "description": "Refund description",
#     "type": "full"
# }
# refund = Refund(data)
