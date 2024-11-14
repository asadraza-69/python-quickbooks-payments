from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.operations.operationsconverter import OperationsConverter


class CaptureDetail:
    def __init__(self, data=None):
        self.created = None
        self.amount = None
        self.context = None
        self.description = None

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
#     "created": "2021-01-01",
#     "amount": 100.0,
#     "context": "Capture context",
#     "description": "Capture description"
# }
# capture_detail = CaptureDetail(data)
