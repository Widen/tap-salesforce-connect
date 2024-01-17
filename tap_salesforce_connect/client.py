"""REST client handling, including SalesforceConnectStream base class."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Callable, Generator, Iterable

import backoff
import requests
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

from tap_salesforce_connect.auth import SalesforceConnectAuthenticator

if sys.version_info >= (3, 8):
    from functools import cached_property
else:
    from cached_property import cached_property

_Auth = Callable[[requests.PreparedRequest], requests.PreparedRequest]
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class SalesforceConnectStream(RESTStream):
    """SalesforceConnect stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return (
            self.config["instance_url"]
            + "/services/data/v57.0/connect/communities/"
            + self.config["community_id"]
        )

    next_page_token_jsonpath = "$.nextPageToken"  # Or override `get_next_page_token`.

    @cached_property
    def authenticator(self) -> _Auth:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return SalesforceConnectAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {
            "Authorization": f"Bearer "  # type: ignore
            f"{self.authenticator.access_token}",
        }
        return headers

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:
        """Return a dictionary of values to be used in URL parameterization.

        Args:
            context: The stream context.
            next_page_token: The next page index or value.

        Returns:
            A dictionary of URL query parameters.
        """
        params: dict = {}
        if next_page_token:
            params["page"] = next_page_token
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

    def post_process(self, row: dict, context: dict | None = None) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # the incoming schemas can be recursive. Because there is no way to provide
        # a recursive schema, any property that is a json object or array
        # will be stringified.
        stringified_row = dict()
        for k, v in row.items():
            if isinstance(v, dict) or isinstance(v, list):
                stringified_row[k] = json.dumps(v)
            else:
                stringified_row[k] = v
        return stringified_row

    # there is a one-hour rate limit on the SalesforceConnect API
    def backoff_wait_generator(self) -> Generator[float, None, None]:
        """Use wait generator for the backoff decorator on request failure.

        See for options:
        https://github.com/litl/backoff/blob/master/backoff/_wait_gen.py

        And see for examples: `Code Samples <../code_samples.html#custom-backoff>`_

        Returns:
            The wait generator
        """
        return backoff.expo(factor=3)  # type: ignore # ignore 'Returning Any'

    def backoff_max_tries(self) -> int:
        """Provide the number of attempts before giving up when retrying requests.

        Returns:
            Number of max retries.
        """
        return 20
