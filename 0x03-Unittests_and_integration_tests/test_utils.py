#!/usr/bin/env python3
"""
Unit tests for utility functions.
"""

import unittest
from unittest.mock import patch, Mock

from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Testing the imported access nested map using parameterized"""
    @parameterized.expand([
        ({'a': 1}, ('a',), 1),
        ({'a': {'b': 2}}, ('a',), {'b': 2}),
        ({'a': {'b': 2}}, ('a', 'b'), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """Test correct access of nested_map."""
        self.assertEqual(
            access_nested_map(nested_map=nested_map, path=path),
            expected
        )

    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ('a', 'b')),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map=nested_map, path=path)


class TestGetJson(unittest.TestCase):
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """Test that get_json returns expected payload."""
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            self.assertEqual(get_json(url=test_url), test_payload)


class TestMemoize(unittest.TestCase):
    def test_memoize(self):
        """Test memoization decorator functionality."""

        class TestClass:
            """Class to test memoization decorator."""

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        obj = TestClass()

        # Patch TestClass.a_method
        with patch.object(TestClass, "a_method", return_value=42) as m_method:
            first_value = obj.a_property
            second_value = obj.a_property

            # Ensure memoized property returns correct values
            self.assertEqual(first_value, 42)
            self.assertEqual(second_value, 42)

            # Ensure underlying method is only called once
            m_method.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=2)
