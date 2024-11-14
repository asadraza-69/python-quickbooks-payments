from .modulesconstants import ModulesConstants
from ..operations import OperationsConverter


class CardPresent:
    def __init__(self, data=None):
        self.track1 = None
        self.track2 = None
        self.ksn = None
        self.pin_block = None

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
#     "track1": "track1 data",
#     "track2": "track2 data",
#     "ksn": "ksn data",
#     "pin_block": "pin block data"
# }
# card_present = CardPresent(data)
