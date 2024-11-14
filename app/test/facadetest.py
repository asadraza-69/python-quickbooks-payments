import unittest
from app.quickbookspayments.operations.operationsconverter import OperationsConverter

class FacadeTest(unittest.TestCase):

    def test_json_decode(self):
        with self.assertRaises(RuntimeError):
            OperationsConverter.object_from("something, is not json}", "Charge")

if __name__ == '__main__':
    unittest.main()
