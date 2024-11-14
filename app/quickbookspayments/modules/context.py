from .modulesconstants import ModulesConstants
from ..operations import OperationsConverter


class Context:
    def __init__(self, data=None):
        self.device_info = None
        self.mobile = None
        self.recurring = None
        self.is_ecommerce = None
        self.tax = None
        self.recon_batch_id = None
        self.payment_grouping_code = None
        self.txn_authorization_stamp = None
        self.payment_status = None
        self.merchant_account_number = None
        self.client_trans_id = None

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
#     "device_info": {"type": "mobile", "model": "iPhone"},
#     "mobile": True,
#     "recurring": False,
#     "is_ecommerce": True,
#     "tax": 10.0,
#     "recon_batch_id": "batch123",
#     "payment_grouping_code": "code123",
#     "txn_authorization_stamp": "stamp123",
#     "payment_status": "completed",
#     "merchant_account_number": "merchant123",
#     "client_trans_id": "trans123"
# }
# context = Context(data)
