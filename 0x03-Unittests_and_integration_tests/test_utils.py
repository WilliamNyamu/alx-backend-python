# Create a TestAccessNestedMap class that inherits from unittest.TestCase.

# Implement the TestAccessNestedMap.test_access_nested_map method to test that the method returns what it is supposed to.

# Decorate the method with @parameterized.expand to test the function for following inputs:

# nested_map={"a": 1}, path=("a",)
# nested_map={"a": {"b": 2}}, path=("a",)
# nested_map={"a": {"b": 2}}, path=("a", "b")
# For each of these inputs, test with assertEqual that the function returns the expected result.


import unittest
from utils import access_nested_map
from parameterized import parameterized

class TestAccessNestedMap(unittest.TestCase):
    pass

if __name__=="__main__":
    unittest.main()