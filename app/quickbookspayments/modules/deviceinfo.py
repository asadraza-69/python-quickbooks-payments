from .modulesconstants import ModulesConstants
from ..operations import OperationsConverter


class DeviceInfo:
    def __init__(self, data=None):
        self.id = None
        self.type = None
        self.longitude = None
        self.latitude = None
        self.encrypted = None
        self.phone_number = None
        self.mac_address = None
        self.ip_address = None

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
#     "id": "device123",
#     "type": "mobile",
#     "longitude": "123.456",
#     "latitude": "78.910",
#     "encrypted": True,
#     "phone_number": "555-5555",
#     "mac_address": "00:1B:44:11:3A:B7",
#     "ip_address": "192.168.1.1"
# }
# device_info = DeviceInfo(data)
