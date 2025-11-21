#!/usr/bin/env python3

import unittest
import client
from client import GithubOrgClient
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized


# class TestGithubOrgClient(unittest.TestCase):
#     """Testing the imported GithubOrgClient class from client.py"""
#     @parameterized.expand([
#         ('google',),
#         ('abc',)
#     ])
#     @patch.object(GithubOrgClient, 'org')
#     def test_org(self, param, mock_org):
#         """Testing the org method"""
#         mock_org.get_json.return_value = {'data': 'values'}
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
    
    def test_public_repos_url(self):
        """Testing the public repos url property"""
        with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repo:
            mock_public_repo.return_value = "https://api.github.com/ant/repos/"
            org_client = GithubOrgClient('ant')
            self.assertEqual(org_client._public_repos_url, "https://api.github.com/ant/repos/")

if __name__=="__main__" :
    unittest.main(verbosity=0)
