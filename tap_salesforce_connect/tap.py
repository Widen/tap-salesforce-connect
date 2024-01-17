"""SalesforceConnect tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th

from tap_salesforce_connect import streams


class TapSalesforceConnect(Tap):
    """SalesforceConnect tap class."""

    name = "tap-salesforce-connect"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "instance_url",
            th.StringType,
            required=True,
            description="The url of your salesforce instance; usually in the format"
            "of `https://<MyDomainName>.my.salesforce.com`",
        ),
        th.Property(
            "client_id",
            th.StringType,
            required=True,
            secret=True,
            description="The consumer key from the connected app.",
        ),
        th.Property(
            "client_secret",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The consumer secret from the connected app.",
        ),
        th.Property(
            "refresh_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the Salesforce Connect API.",
        ),
        th.Property(
            "community_id",
            th.StringType,
            required=True,
            description="The community ids targeted for replication.",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.SalesforceConnectStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.TopicFeedStream(self),
            streams.UsersStream(self),
            streams.TopicsStream(self),
            streams.CommentsStream(self),
        ]


if __name__ == "__main__":
    TapSalesforceConnect.cli()
