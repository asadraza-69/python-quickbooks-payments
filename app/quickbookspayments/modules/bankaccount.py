from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.modules.entity import Entity
from app.quickbookspayments.operations.operationsconverter import OperationsConverter



class BankAccount(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.updated = None
        self.name = None
        self.routing_number = None
        self.account_number = None
        self.input_type = None
        self.account_type = None
        self.phone = None
        self.country = None
        self.bank_name = None
        self.bank_code = None
        self.default = None
        self.entity_version = None
        self.entity_id = None
        self.entity_type = None

        if data is not None:
            for name, value in data.items():
                if hasattr(self, name):
                    if value is not None:
                        if isinstance(value, dict):
                            class_name = getattr(ModulesConstants, 'NAMESPACE_MODULES') + OperationsConverter.to_upper_case_class_name(name)
                            obj = globals()[class_name](value)
                            setattr(self, name, obj)
                        else:
                            setattr(self, name, value)

# Example Usage:
# data = {
#     "updated": "2021-01-01",
#     "name": "John Doe",
#     "routing_number": "123456789",
#     "account_number": "987654321",
#     "input_type": "manual",
#     "account_type": "savings",
#     "phone": "555-5555",
#     "country": "USA",
#     "bank_name": "Bank of the World",
#     "bank_code": "BW123",
#     "default": True,
#     "entity_version": "1.0",
#     "entity_id": "abc123",
#     "entity_type": "individual"
# }
# bank_account = BankAccount(data)
