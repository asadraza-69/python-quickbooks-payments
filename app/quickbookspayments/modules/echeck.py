from app.quickbookspayments.modules.entity import Entity
from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.operations.operationsconverter import OperationsConverter


class ECheck(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.status = None
        self.amount = None
        self.bank_account = None
        self.token = None
        self.context = None
        self.description = None
        self.payment_mode = None
        self.check_number = None
        self.auth_code = None
        self.refund_detail = None
        self.type = None
        self.bank_account_on_file = None

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
#     "bank_account": {"account_number": "123456789", "routing_number": "987654321"},
#     "token": "token123",
#     "context": {"device_info": "device123"},
#     "description": "Payment description",
#     "payment_mode": "eCheck",
#     "check_number": "000123",
#     "auth_code": "auth123",
#     "refund_detail": {"amount": 50.0, "date": "2021-01-01"},
#     "type": "sale",
#     "bank_account_on_file": True
# }
# echeck = ECheck(data)
