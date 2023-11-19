import unittest
from dynamic_sequens_diagram import has_returned_object_type

class TestHasReturnedObjectType(unittest.TestCase):

    def test_no_return_instruction(self):
        # Test when there is no "return" instruction in the bytecode
        bytecode = [
            {"opr": "invoke", "type": "SomeType"},
            {"opr": "other", "type": "AnotherType"}
        ]
        result = has_returned_object_type(bytecode, "TestClass")
        self.assertFalse(result[0])  # Expecting False
        self.assertIsNone(result[1])

    def test_return_without_type(self):
        # Test when there is a "return" instruction, but the type is None
        bytecode = [
            {"opr": "return", "type": None},
            {"opr": "invoke", "type": "SomeType"}
        ]
        result = has_returned_object_type(bytecode, "TestClass")
        self.assertFalse(result[0])  # Expecting False
        self.assertIsNone(result[1])

    def test_return_with_type(self):
        # Test when there is a "return" instruction with a non-None type
        bytecode = [
            {"opr": "return", "type": "ReturnType"},
            {"opr": "invoke", "type": "SomeType"}
        ]
        result = has_returned_object_type(bytecode, "TestClass")
        self.assertTrue(result[0])  # Expecting True
        self.assertEqual(result[1], "ReturnType")


if __name__ == '__main__':
    unittest.main()
