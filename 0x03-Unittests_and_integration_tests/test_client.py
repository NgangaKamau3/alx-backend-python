#!/usr/bin/env python3
"""
test_client module
"""
import unittest
from typing import Dict
from parameterized import parameterized, parameterized_class

from client import GithubOrgClient

from unittest.mock import (
    MagicMock,
    patch,
    PropertyMock,
    Mock
    )

from fixtures import TEST_PAYLOAD
from requests import HTTPError


class TestGithubOrgClient(unittest.TestCase):
    """Test for the GithubOrgClient class"""

    test_data = (
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"}),
    )

    @parameterized.expand(test_data)
    @patch("client.get_json")
    def test_org(self, org: str, response: Dict,
                 mocked_func: MagicMock) -> None:
        """test for org method"""
        mocked_func.return_value = MagicMock(return_value=response)
        github_org_client = GithubOrgClient(org)
        self.assertEqual(github_org_client.org(), response)

        mocked_func.assert_called_once_with(
            f"https://api.github.com/orgs/{org}")

    def test_public_repos_url(self) -> None:
        """test for the public_repos_url property"""
        with patch(
                "client.GithubOrgClient.org",
                new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos"
                }
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/users/google/repos")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """test for the public_repos method"""
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos",
            "repos": [
                {
                 "id": 7776515,
                 "name": "cpp-netlib",
                 "private": False,
                 "owner": {
                        "login": "google",
                        "id": 1342004,
                        },
                 "fork": True,
                 "url": "https://api.github.com/repos/google/cpp-netlib",
                 "created_at": "2013-01-23T14:45:32Z",
                 "updated_at": "2019-11-15T02:26:31Z",
                 "has_issues": False,
                 "forks": 59,
                 "default_bracnch": "master",
                    },
                {
                 "id": 7968417,
                 "name": "dagger",
                 "private": False,
                 "owner": {
                        "login": "google",
                        "id": 1342004,
                        },
                 "fork": True,
                 "url": "https://api.github.com/repos/google/dagger",
                 "created_at": "2013-02-01T23:14:14Z",
                 "updated_at": "2019-12-03T12:39:55Z",
                 "has_issues": True,
                 "forks": 1741,
                 "default_bracnch": "master",
                    },
                ]
            }
        mock_get_json.return_value = test_payload['repos']
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                ["cpp-netlib", "dagger"])
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    parameters = (
        ({"license": {"key": "bsl-1.0"}}, "bsl-1.0", True),
        ({"license": {"key":  "apache-2.0"}}, "bsl-1.0", False)
    )

    @parameterized.expand(parameters)
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """test for the has_license method"""
        github_org_client = GithubOrgClient("google")
        client_has_license = github_org_client.has_license(repo, key)
        self.assertEqual(client_has_license, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration test for the GithubOrgClient class"""

    @classmethod
    def setUpClass(cls) -> None:
        """setup class fixtures"""
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{"json.return_value": route_payload[url]})
            return HTTPError
        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """test for the public_repos method"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos)

    def test_public_repos_with_license(self) -> None:
        """test for the public_repos method with a license"""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos)

    @classmethod
    def tearDownClass(cls):
        """Remove the class fixtures"""
        cls.get_patcher.stop()


if __name__ == "__main__":
    unittest.main()