#!/usr/bin/env python3

import unittest
import client
from client import GithubOrgClient
from unittest.mock import patch, Mock
from parameterized import parameterized


# class TestGithubOrgClient(unittest.TestCase):
#     @patch('client.GithubOrgClient')
#     @parameterized.expand([
#         ('google'),
#         ('abc')
#     ])
#     def test_org(self, mock_org, param):
#         mock = Mock()
#         mock(param).org.get_json.return_value = {'data':'values'}
#         mock_org = mock

#         self.assertEqual(GithubOrgClient(param).org, mock_org)




class TestGithubOrgClient(unittest.TestCase):
    """Testing the imported GithubOrgClient class from client.py"""
    @parameterized.expand([
        ('google'),
        ('abc')
    ])
    def test_org(self, param):
        """Testing the org method"""
        with patch.object(GithubOrgClient, 'org') as mock_org:
            mock_org.get_json.return_value = {'data': 'values'}

            self.assertEqual(GithubOrgClient(param).org, mock_org)

if __name__=="__main__" :
    unittest.main(verbosity=0)
