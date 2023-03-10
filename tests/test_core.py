"""Tests standard tap features using the built-in SDK tests library."""

from singer_sdk.testing import get_tap_test_class

from tap_salesforce_connect.tap import TapSalesforceConnect


SAMPLE_CONFIG = {
    "instance_url": "instance_url_value",
    "client_id": "client_id_value",
    "client_secret": "client_secret_value",
    "refresh_token": "refresh_token_value",
    "community_id": "community_id_value",
}


def url_path(path: str = "/chatter/feeds/news/me/feed-elements") -> str:
    """Utility function returning a common url for mocked API calls.

    Args:
        path: a path to add to the end of the base url.

    Returns:
        A full url.
    """
    return "https://MyDomainName.my.salesforce.com" + \
           "services/data/v29.0/connect/communities/internal" + \
           path


def test_standard_tap_tests(requests_mock):
    """Run standard built-in tap tests from the SDK"""
    requests_mock.get(url_path(), json={"users": []})
    TestTapSalesforceConnect = get_tap_test_class(
        tap_class=TapSalesforceConnect,
        config=SAMPLE_CONFIG
    )
