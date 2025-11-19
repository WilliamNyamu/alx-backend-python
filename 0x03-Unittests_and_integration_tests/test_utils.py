# Create a TestAccessNestedMap class that inherits from unittest.TestCase.

# Implement the TestAccessNestedMap.test_access_nested_map method to test that the method returns what it is supposed to.

# Decorate the method with @parameterized.expand to test the function for following inputs:

# nested_map={"a": 1}, path=("a",)
# nested_map={"a": {"b": 2}}, path=("a",)
# nested_map={"a": {"b": 2}}, path=("a", "b")
# For each of these inputs, test with assertEqual that the function returns the expected result.


import unittest
from utils import access_nested_map, get_json, memoize
from parameterized import parameterized
from unittest.mock import patch, Mock
import utils


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({'a': 1}, ("a"), 1),
        ({'a': {'b': 2}}, ('a'), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map=nested_map, path=path), expected)
    
    @parameterized.expand([
        ({}, ("a")),
        ({'a': 1}, ('a','b')),
    ])
    def test_access_nested_map_exception(self, nested_path, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map=nested_path, path=path)


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        with patch('utils.requests.get') as mock_get:
            mock_requests = Mock()
            mock_requests.json.return_value = test_payload
            mock_get.return_value = mock_requests
            self.assertEqual(get_json(url=test_url), test_payload)



class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        # Define a local class to test the memoize decorator
        class TestClass:
            # Simple method that we will later patch
            def a_method(self):
                return 42

            # Apply the memoize decorator to convert this method into
            # a cached property. The first access calls a_method(),
            # and the result is stored as an attribute (e.g., _a_property).
            @memoize
            def a_property(self):
                return self.a_method()

        # Instantiate the test class
        obj = TestClass()

        # Patch TestClass.a_method so we can track how many times it is called.
        # patch.object is required because TestClass is defined locally here.
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # First access should call the real (mocked) method
            first_value = obj.a_property

            # Second access should return the cached value, NOT call a_method again
            second_value = obj.a_property

            # Ensure the returned values are correct
            self.assertEqual(first_value, 42)
            self.assertEqual(second_value, 42)

            # Because of memoization, a_method should only be called once
            mock_method.assert_called_once()              

if __name__=="__main__":
    unittest.main(verbosity=2)