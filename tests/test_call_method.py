import json
import unittest
import os
from unittest.mock import mock_open, patch

from dynamic_sequens_diagram import call_method
from unittest.mock import MagicMock

class TestCallMethod(unittest.TestCase):

    def setUp(self):
        # Set up any necessary resources or test data
        os.remove("test_output.puml") # remove output file if it exists
        self.bytecode = [{
            "offset": 0,
            "opr": "load",
            "type": "ref",
            "index": 0
          },
          {
            "offset": 1,
            "opr": "invoke",
            "access": "special",
            "method": {
              "is_interface": False,
              "ref": {
                "kind": "class",
                "name": "foo"
              },
              "name": "bar",
              "args": [],
              "returns": None
            }
          },
          {
            "offset": 4,
            "opr": "return",
            "type": None
          }]
        self.output_file = open("test_output.puml", "w")


    def test_call_method_with_args_and_output_file(self):
        self.output_file = open("test_output.puml", "w")
        self.output_file.write("@startuml\n")
        # Test when the method is called without any arguments
        call_method(self.bytecode, self.output_file, "bar" )
        self.output_file.write("@enduml\n")
        self.output_file.close()
        with open("test_output.puml", "r") as fp:
            file_content = fp.read()
            expected_string = ("@startuml\n"
                               "ar -> Foo : bar()\n"
                               "activate Foo\n"
                               "Foo --> Bar : bar()\nd"
                               "eactivate Foo\n"
                               "@enduml\n")
        self.assertIn(expected_string, file_content, f"File doesn't contain the expected string: {expected_string}")


    def test_method_ignor_calling_method_with_java_args(self):
        self.bytecode = [{
            "offset": 0,
            "opr": "load",
            "type": "ref",
            "index": 0
          },
          {
            "offset": 1,
            "opr": "invoke",
            "access": "special",
            "method": {
              "is_interface": False,
              "ref": {
                "kind": "class",
                "name": "java/bar"
              },
              "name": "java/bar",
              "args": [],
              "returns": None
            }
          }]
        result = call_method(self.bytecode, self.output_file, "foo")
        with open("test_output.puml", "r") as fp:
            file_content = fp.read()
        self.assertEqual(file_content, "", f"File is not empty. Content: {file_content}")



    def test_call_method_without_invoked_method_name (self):
        self.bytecode = [{
            "offset": 0,
            "opr": "load",
            "type": "ref",
            "index": 0
        },
            {
                "offset": 1,
                "opr": "invoke",
                "access": "special",
                "method": {
                    "is_interface": False,
                    "ref": {
                        "kind": "class",
                    },
                    "args": [],
                    "returns": None
                }
            }]
        result = call_method(self.bytecode, self.output_file, "foo")
        with open("test_output.puml", "r") as fp:
            file_content = fp.read()
        self.assertEqual(file_content, "", f"File is not empty. Content: {file_content}")
    def test_call_method_without_called_method (self):
        result = call_method(self.bytecode, self.output_file, None)
        with open("test_output.puml", "r") as fp:
            file_content = fp.read()
        self.assertEqual(file_content, "", f"File is not empty. Content: {file_content}")



if __name__ == '__main__':
    with open("Diagrams/TestUnitDiagram.puml", "w") as my_file:
        unittest.main()
