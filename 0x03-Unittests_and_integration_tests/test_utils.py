#!/usr/bin/env python3
"""test cases for utils module"""

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized

from utils import (
    access_nested_map,
    get_json,
    memoize
    )


class TestAccessNestedMap(unittest.TestCase):
    """Test cases for the utils functions"""

    # Define the test data as a list of tuples:
    # (input_a, input_b, expected_result)
    test_parameters = (
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
        )

    test_parameter_2 = (
        ({}, ("a",)),
        ({"a": 1}, ("a", "b"))
        )

    @parameterized.expand(test_parameters)
    def test_access_nested_map(self, nested_map, path, expected_result):
        """Test case for the access_nested_map function"""
        res = access_nested_map(nested_map, path)
        self.assertEqual(res, expected_result)

    @parameterized.expand(test_parameter_2)
    def test_access_nested_map_exception(self, nested_map, path):
        """Test case for the access_nested_map exceptions"""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Test cases for GetJson methods."""

    test_parameter_3 = (
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    )

    @parameterized.expand(test_parameter_3)
    def test_get_json(self, test_url, test_payload):
        """Test case for getjson function"""
        atrributes = {'json.return_value': test_payload}

        with patch("requests.get", return_value=Mock(**atrributes)) as req_get:
            self.assertEqual(get_json(test_url), test_payload)
            req_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test the memoize function"""

    def test_memoize(self):
        """Test memoize output"""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        with patch.object(TestClass, "a_method",
                          return_value=lambda: 42,) as memoize_func:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)

            memoize_func.assert_called_once()


if __name__ == "__main__":
    unittest.main()
