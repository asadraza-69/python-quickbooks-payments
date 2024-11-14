from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.operations.operationsconverter import OperationsConverter


class Address:
    def __init__(self, data=None):
        self.street_address = None
        self.city = None
        self.region = None
        self.country = None
        self.postal_code = None

        if data is not None:
            for name, value in data.items():
                if hasattr(self, name):
                    if value is not None:
                        if isinstance(value, dict):
                            class_name = getattr(
                                ModulesConstants, 'NAMESPACE_MODULES') + OperationsConverter.to_upper_case_class_name(
                                name)
                            obj = globals()[class_name](value)  # Dynamically instantiate the class
                            setattr(self, name, obj)
                        else:
                            setattr(self, name, value)

# Example Usage:
# data = {
#     "street_address": "123 Main St",
#     "city": "Springfield",
#     "region": "IL",
#     "country": "USA",
#     "postal_code": "62701"
# }
# address = Address(data)
