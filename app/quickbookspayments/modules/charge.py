from app.quickbookspayments.modules.entity import Entity
from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.operations.operationsconverter import OperationsConverter



class Charge(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.status = None
        self.amount = None
        self.currency = None
        self.token = None
        self.card = None
        self.context = None
        self.description = None
        self.auth_code = None
        self.capture_detail = None
        self.refund_detail = None
        self.capture = None
        self.avs_street = None
        self.avs_zip = None
        self.card_security_code_match = None
        self.app_type = None
        self.card_on_file = None
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
#     "status": "completed",
#     "amount": 100.0,
#     "currency": "USD",
#     "token": "token123",
#     "card": {"number": "4111111111111111", "exp_month": 12, "exp_year": 2025},
#     "context": "transaction context",
#     "description": "transaction description",
#     "auth_code": "auth123",
#     "capture_detail": {"created": "2021-01-01", "amount": 100.0},
#     "refund_detail": {"created": "2021-01-02", "amount": 50.0},
#     "capture": "capture data",
#     "avs_street": "123 Main St",
#     "avs_zip": "62701",
#     "card_security_code_match": "Y",
#     "app_type": "e-commerce",
#     "card_on_file": True,
#     "type": "sale"
# }
# charge = Charge(data)
