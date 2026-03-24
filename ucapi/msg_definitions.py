"""
Internal WebSocket message structure definitions.

See Integration-API for more information:
https://github.com/unfoldedcircle/core-api/tree/main/integration-api

:copyright: (c) 2026 by Unfolded Circle ApS.
:license: MPL-2.0, see LICENSE for more details.
"""

from dataclasses import dataclass

from .media_player import BrowseOptions, SearchMediaFilter


@dataclass(kw_only=True)
class BrowseMediaMsgData(BrowseOptions):
    """
    Browsing media request message.

    Attributes:
        entity_id (str):
            media-player entity ID to browse.
    """

    entity_id: str

    def __post_init__(self):  # pylint: disable=W0246
        """Encode custom fields."""
        super().__post_init__()


@dataclass(kw_only=True)
class SearchMediaMsgData(BrowseOptions):
    """
    Search media request message.

    Attributes:
        entity_id (str):
            media-player entity ID to browse.
        query (str):
            Free text search query.
        filter (SearchMediaFilter|None):
            Additional user filter to limit the search scope.
    """

    entity_id: str
    query: str
    filter: SearchMediaFilter | None = None

    def __post_init__(self):
        """Encode custom fields."""
        super().__post_init__()
        if isinstance(self.filter, dict):
            self.filter = SearchMediaFilter(**self.filter)
