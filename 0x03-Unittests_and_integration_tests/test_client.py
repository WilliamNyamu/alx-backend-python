#!/usr/bin/env python3
"""Unit tests for the GithubOrgClient class.

This module contains test cases for testing the GithubOrgClient class
from the client module. It uses unittest, mock, and parameterized
for comprehensive testing.
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class.

    This class tests various methods and properties of GithubOrgClient
    including org, _public_repos_url, and public_repos.
    """

    @parameterized.expand([
        ('google',),
        ('abc',)
    ])
    def test_org(self, param):
        """Test that the org method returns the correct value.

        Args:
            param: The organization name to test with.
        """
        with patch.object(GithubOrgClient, 'org') as mock_org:
            mock_org.get_json.return_value = {'data': 'values'}
            self.assertEqual(GithubOrgClient(param).org, mock_org)

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the correct URL.

        This test mocks the org property to return a known payload
        and verifies that _public_repos_url extracts the repos_url
        correctly.
        """
        with patch.object(
            GithubOrgClient,
            'org',
            new_callable=PropertyMock
        ) as mock_org:
            mock_org.return_value = {
                "repos_url": "https://api.github.com/orgs/ant/repos"
            }
            org_client = GithubOrgClient('ant')
            self.assertEqual(
                org_client._public_repos_url,
                "https://api.github.com/orgs/ant/repos"
            )

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list of repos.

        This test mocks get_json to return a known payload and mocks
        _public_repos_url to return a known URL. It verifies that
        public_repos returns the correct list of repository names
        and that the mocked functions were called appropriately.

        Args:
            mock_get_json: Mock object for the get_json function.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        with patch.object(
            GithubOrgClient,
            '_public_repos_url',
            new_callable=PropertyMock
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = (
                "https://api.github.com/orgs/ant/repos"
            )

            org_client = GithubOrgClient('ant')
            result = org_client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()


if __name__ == "__main__":
    unittest.main(verbosity=0)
