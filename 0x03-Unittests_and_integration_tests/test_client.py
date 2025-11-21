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
        # Patching the GithubOrgClient.org and making it return a known payload.
        with patch.object(GithubOrgClient, 'org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "https://api.github.com/orgs/ant/repos"}
            org_client = GithubOrgClient('ant')
            self.assertEqual(org_client._public_repos_url, "https://api.github.com/orgs/ant/repos")
    
@patch('client.get_json')
def test_public_repos(self, mock_get_json):
    """Testing the public_repos method"""
    # Set up the payload that get_json will return
    mock_get_json.return_value = [
        {"name": "repo1"},
        {"name": "repo2"},
        {"name": "repo3"}
    ]
    
    with patch.object(GithubOrgClient, '_public_repos_url', new_callable=PropertyMock) as mock_public_repos_url:
        mock_public_repos_url.return_value = "https://api.github.com/orgs/ant/repos"
        
        org_client = GithubOrgClient('ant')
        result = org_client.public_repos()
        
        # Test that the list of repos matches expected
        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        
        # Test that mocked property was called once
        mock_public_repos_url.assert_called_once()
        
        # Test that mocked get_json was called once
        mock_get_json.assert_called_once()

        

if __name__=="__main__" :
    unittest.main(verbosity=0)
