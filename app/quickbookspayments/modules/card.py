from app.quickbookspayments.modules.entity import Entity
from app.quickbookspayments.modules.modulesconstants import ModulesConstants
from app.quickbookspayments.operations.operationsconverter import OperationsConverter


class Card(Entity):
    def __init__(self, data=None):
        super().__init__()
        self.updated = None
        self.name = None
        self.number = None
        self.address = None
        self.commercial_card_code = None
        self.cvc_verification = None
        self.card_type = None
        self.exp_month = None
        self.exp_year = None
        self.default = None
        self.is_business = None
        self.is_level3_eligible = None
        self.cvc = None
        self.entity_version = None
        self.entity_id = None
        self.entity_type = None
        self.zero_dollar_verification = None

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
#     "updated": "2021-01-01",
#     "name": "John Doe",
#     "number": "4111111111111111",
#     "address": {"street": "123 Main St", "city": "Springfield", "state": "IL", "zip": "62701"},
#     "commercial_card_code": "123",
#     "cvc_verification": "Y",
#     "card_type": "VISA",
#     "exp_month": 12,
#     "exp_year": 2025,
#     "default": True,
#     "is_business": False,
#     "is_level3_eligible": True,
#     "cvc": "123",
#     "entity_version": "1.0",
#     "entity_id": "abc123",
#     "entity_type": "individual",
#     "zero_dollar_verification": False
# }
# card = Card(data)
