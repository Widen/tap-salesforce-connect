"""Stream type classes for tap-salesforce-connect."""

from __future__ import annotations

from typing import Optional

from singer_sdk import typing as th

from tap_salesforce_connect.client import SalesforceConnectStream

# common properties
url_property = th.Property("url", th.StringType)
id_property = th.Property("id", th.StringType)
type_property = th.Property("type", th.StringType)
created_date_property = th.Property("createdDate", th.DateTimeType)
name_property = th.Property("name", th.StringType)


class UsersStream(SalesforceConnectStream):
    """Define Users stream."""

    name = "users"
    path = "/chatter/users"
    records_jsonpath = "$.users[*]"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("aboutMe", th.StringType),
        th.Property("address", th.StringType),
        th.Property("bannerPhoto", th.StringType),
        th.Property("chatterActivity", th.StringType),
        th.Property("chatterInfluence", th.StringType),
        th.Property("companyName", th.StringType),
        th.Property("currentStatus", th.StringType),
        th.Property("email", th.StringType),
        th.Property("followersCount", th.IntegerType),
        th.Property("followingCounts", th.StringType),
        th.Property("groupCount", th.IntegerType),
        th.Property("hasChatter", th.BooleanType),
        th.Property("managerId", th.StringType),
        th.Property("managerName", th.StringType),
        th.Property("phoneNumbers", th.StringType),
        th.Property("thanksReceived", th.IntegerType),
        th.Property("username", th.StringType),
        th.Property("additionalLabel", th.StringType),
        th.Property("communityNickname", th.StringType),
        th.Property("companyName", th.StringType),
        th.Property("displayName", th.StringType),
        th.Property("firstName", th.StringType),
        id_property,
        th.Property("isActive", th.BooleanType),
        th.Property("isChatterGuest", th.BooleanType),
        th.Property("isInThisCommunity", th.BooleanType),
        th.Property("lastName", th.StringType),
        th.Property("motif", th.StringType),
        th.Property("mySubscription", th.StringType),
        name_property,
        th.Property("outOfOffice", th.StringType),
        th.Property("photo", th.StringType),
        th.Property("reputation", th.StringType),
        th.Property("stamps", th.StringType),
        th.Property("title", th.StringType),
        type_property,
        url_property,
        th.Property("userType", th.StringType),
    ).to_dict()


class TopicsStream(SalesforceConnectStream):
    """Define Topcis stream."""

    name = "topics"
    path = "/topics"
    records_jsonpath = "$.topics[*]"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        created_date_property,
        th.Property("description", th.StringType),
        id_property,
        th.Property("images", th.StringType),
        th.Property("isBeingDeleted", th.BooleanType),
        name_property,
        th.Property("nonLocalizedName", th.StringType),
        th.Property("talkingAbout", th.IntegerType),
        url_property,
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "topic_id": record["id"],
        }


class TopicFeedStream(SalesforceConnectStream):
    """Define child Topic Feed stream."""

    parent_stream_type = TopicsStream
    name = "topic_feed"
    path = "/chatter/feeds/topics/{topic_id}/feed-elements"
    records_jsonpath = "$.elements[*]"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("actor", th.StringType),
        th.Property("attachment", th.StringType),
        th.Property("body", th.StringType),
        th.Property("canShare", th.BooleanType),
        th.Property("capabilities", th.StringType),
        th.Property("clientInfo", th.StringType),
        th.Property("comments", th.StringType),
        created_date_property,
        th.Property("currentUserLike", th.StringType),
        th.Property("event", th.BooleanType),
        th.Property("feedElementType", th.StringType),
        th.Property("hasVerifiedComment", th.BooleanType),
        th.Property("header", th.StringType),
        id_property,
        th.Property("isBookmarkedByCurrentUser", th.BooleanType),
        th.Property("isDeleteRestricted", th.BooleanType),
        th.Property("isLikedByCurrentUser", th.BooleanType),
        th.Property("isSharable", th.BooleanType),
        th.Property("likes", th.StringType),
        th.Property("likesMessage", th.StringType),
        th.Property("modifiedDate", th.DateTimeType),
        th.Property("moderationFlags", th.StringType),
        th.Property("myLike", th.StringType),
        th.Property("originalFeedItem", th.StringType),
        th.Property("originalFeedItemActor", th.StringType),
        th.Property("parent", th.StringType),
        th.Property("photoUrl", th.StringType),
        th.Property("preamble", th.StringType),
        th.Property("relativeCreatedDate", th.StringType),
        th.Property("topics", th.StringType),
        type_property,
        url_property,
        th.Property("visibility", th.StringType),
    ).to_dict()

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        """Return a context dictionary for child streams."""
        return {
            "feed_element_id": record["id"],
        }


class CommentsStream(SalesforceConnectStream):
    """Define child Comments stream."""

    parent_stream_type = TopicFeedStream
    name = "comments"
    path = "/chatter/feed-elements/{feed_element_id}/capabilities/comments/items"
    records_jsonpath = "$.items[*]"
    primary_keys = ["id"]
    replication_key = None
    schema = th.PropertiesList(
        th.Property("attachment", th.StringType),
        th.Property("body", th.StringType),
        th.Property("capabilities", th.StringType),
        th.Property("clientInfo", th.StringType),
        created_date_property,
        th.Property("feedElement", th.StringType),
        th.Property("feedItem", th.StringType),
        id_property,
        th.Property("isDeletable", th.BooleanType),
        th.Property("isDeleteRestricted", th.BooleanType),
        th.Property("likes", th.StringType),
        th.Property("likesMessage", th.StringType),
        th.Property("myLike", th.StringType),
        th.Property("parent", th.StringType),
        th.Property("relativeCreatedDate", th.StringType),
        th.Property("threadLevel", th.IntegerType),
        th.Property("threadParentId", th.StringType),
        type_property,
        url_property,
        th.Property("user", th.StringType),
    ).to_dict()
