"""
API definitions.

:copyright: (c) 2023 by Unfolded Circle ApS.
:license: MPL-2.0, see LICENSE for more details.
"""

import dataclasses
from dataclasses import dataclass, field, fields
from enum import Enum, IntEnum
from typing import Any, Awaitable, Callable, TypeAlias


class DeviceStates(str, Enum):
    """Device states."""

    CONNECTED = "CONNECTED"
    CONNECTING = "CONNECTING"
    DISCONNECTED = "DISCONNECTED"
    ERROR = "ERROR"


class StatusCodes(IntEnum):
    """Response status codes."""

    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    TIMEOUT = 408
    CONFLICT = 409
    SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    SERVICE_UNAVAILABLE = 503


class IntegrationSetupError(str, Enum):
    """More detailed error reason for ``state: ERROR`` condition."""

    NONE = "NONE"
    NOT_FOUND = "NOT_FOUND"
    CONNECTION_REFUSED = "CONNECTION_REFUSED"
    AUTHORIZATION_ERROR = "AUTHORIZATION_ERROR"
    TIMEOUT = "TIMEOUT"
    OTHER = "OTHER"


# Does WsMessages need to be public?
class WsMessages(str, Enum):
    """WebSocket request messages from Remote Two/3."""

    AUTHENTICATION = "authentication"
    GET_DRIVER_VERSION = "get_driver_version"
    GET_DEVICE_STATE = "get_device_state"
    GET_AVAILABLE_ENTITIES = "get_available_entities"
    GET_ENTITY_STATES = "get_entity_states"
    SUBSCRIBE_EVENTS = "subscribe_events"
    UNSUBSCRIBE_EVENTS = "unsubscribe_events"
    ENTITY_COMMAND = "entity_command"
    GET_DRIVER_METADATA = "get_driver_metadata"
    SETUP_DRIVER = "setup_driver"
    SET_DRIVER_USER_DATA = "set_driver_user_data"
    BROWSE_MEDIA = "browse_media"
    SEARCH_MEDIA = "search_media"


# Does WsMsgEvents need to be public?
class WsMsgEvents(str, Enum):
    """WebSocket event messages from Remote Two/3."""

    CONNECT = "connect"
    DISCONNECT = "disconnect"
    ENTER_STANDBY = "enter_standby"
    EXIT_STANDBY = "exit_standby"
    DRIVER_VERSION = "driver_version"
    DEVICE_STATE = "device_state"
    AVAILABLE_ENTITIES = "available_entities"
    ENTITY_STATES = "entity_states"
    ENTITY_CHANGE = "entity_change"
    DRIVER_METADATA = "driver_metadata"
    DRIVER_SETUP_CHANGE = "driver_setup_change"
    ABORT_DRIVER_SETUP = "abort_driver_setup"
    ASSISTANT_EVENT = "assistant_event"
    MEDIA_BROWSE = "media_browse"
    MEDIA_SEARCH = "media_search"


class Events(str, Enum):
    """Internal library events.

    All event parameters are named parameters and optional.
    """

    CLIENT_CONNECTED = "client_connected"
    """WebSocket client connected.

    Named parameters:

    - websocket: WebSocket client connection
    """
    CLIENT_DISCONNECTED = "client_disconnected"
    """WebSocket client disconnected.

    Named parameters:

    - websocket: WebSocket client connection
    """
    ENTITY_ATTRIBUTES_UPDATED = "entity_attributes_updated"
    """Entity attributes updated.

    Named parameters:

    - entity_id: entity identifier
    - entity_type: entity type
    - attributes: updated attributes"""
    SUBSCRIBE_ENTITIES = "subscribe_entities"
    """Integration API `subscribe_events` message.

    Named parameters:

    - entity_ids: list of entity IDs to subscribe to
    - websocket: WebSocket client connection
    """
    UNSUBSCRIBE_ENTITIES = "unsubscribe_entities"
    """Integration API `unsubscribe_events` message.

    Named parameters:

    - entity_ids: list of entity IDs to unsubscribe
    - websocket: WebSocket client connection
    """
    CONNECT = "connect"
    """Integration-API `connect` event message.

    Named parameters:

    - websocket: WebSocket client connection
    """
    DISCONNECT = "disconnect"
    """Integration-API `disconnect` event message.

    Named parameters:

    - websocket: WebSocket client connection
    """
    ENTER_STANDBY = "enter_standby"
    """Integration-API `enter_standby` event message.

    Named parameters:

    - websocket: WebSocket client connection
    """
    EXIT_STANDBY = "exit_standby"
    """Integration-API `exit_standby` event message.

    Named parameters:

    - websocket: WebSocket client connection
    """


# Does EventCategory need to be public?
class EventCategory(str, Enum):
    """Event categories."""

    DEVICE = "DEVICE"
    ENTITY = "ENTITY"


class SetupDriver:
    """Driver setup request base class."""


@dataclass
class DriverSetupRequest(SetupDriver):
    """
    Start driver setup.

    If a driver includes a ``setup_data_schema`` object in its driver metadata, it
    enables the dynamic driver setup process. The setup process can be a simple
    "start-confirm-done" between the Remote Two/3 and the integration driver, or a fully
    dynamic, multistep process with user interactions, where the user has to provide
    additional data or select different options.

    If the initial setup page contains input fields and not just text, the input values
    are returned in the ``setup_data`` dictionary. The key is the input field
    identifier, value contains the input value.
    """

    reconfigure: bool
    setup_data: dict[str, str]


@dataclass
class UserDataResponse(SetupDriver):
    """
    Provide requested driver setup data to the integration driver in a setup process.

    The ``input_values`` dictionary contains the user input data. The key is the input
    field identifier, value contains the input value.
    """

    input_values: dict[str, str]


@dataclass
class UserConfirmationResponse(SetupDriver):
    """
    Provide user confirmation response to the integration driver in a setup process.

    The ``confirm`` field is set to ``true`` if the user had to perform an action like
    pressing a button on a device and then confirms the action with continuing the
    setup process.
    """

    confirm: bool


@dataclass
class AbortDriverSetup(SetupDriver):
    """
    Abort notification.

    - ``error == OTHER``: the user cancelled the setup flow.
    - ``error == TIMEOUT``: timeout occurred, most likely because of no user input.
    """

    error: IntegrationSetupError


class SetupAction:
    """Setup action response base class."""


@dataclass
class RequestUserInput(SetupAction):
    """Setup action to request user input."""

    title: str | dict[str, str]
    settings: list[dict[str, Any]]


@dataclass
class RequestUserConfirmation(SetupAction):
    """Setup action to request a user confirmation."""

    title: str | dict[str, str]
    header: str | dict[str, str] | None = None
    image: str | None = None
    footer: str | dict[str, str] | None = None


@dataclass
class SetupError(SetupAction):
    """Setup action to abort setup process due to an error."""

    error_type: IntegrationSetupError = IntegrationSetupError.OTHER


class SetupComplete(SetupAction):
    """Setup action to complete a successful setup process."""


CommandHandler: TypeAlias = Callable[
    [Any, str, dict[str, Any] | None, Any | None], Awaitable[StatusCodes]
]
"""Entity command handler signature.

Parameters:

- entity: entity instance
- cmd_id: command identifier
- params: optional command parameters
- websocket: optional client connection for sending directed events

Returns: status code
"""


SetupHandler: TypeAlias = Callable[[SetupDriver], Awaitable[SetupAction]]


# ---------------------------------------------------------------------------
# Assistant event message definitions
# ---------------------------------------------------------------------------


class AssistantEventType(str, Enum):
    """Type discriminator for assistant event messages."""

    READY = "ready"
    STT_RESPONSE = "stt_response"
    TEXT_RESPONSE = "text_response"
    SPEECH_RESPONSE = "speech_response"
    FINISHED = "finished"
    ERROR = "error"


class AssistantErrorCode(str, Enum):
    """Error codes for assistant processing."""

    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    INVALID_AUDIO = "INVALID_AUDIO"
    NO_TEXT_RECOGNIZED = "NO_TEXT_RECOGNIZED"
    INTENT_FAILED = "INTENT_FAILED"
    TTS_FAILED = "TTS_FAILED"
    TIMEOUT = "TIMEOUT"
    UNEXPECTED_ERROR = "UNEXPECTED_ERROR"


@dataclass
class AssistantSttResponse:
    """Transcription result of the user's speech input."""

    text: str


@dataclass
class AssistantTextResponse:
    """Textual response and success flag for the processed command."""

    success: bool
    text: str


@dataclass
class AssistantSpeechResponse:
    """Reference to a TTS audio response provided by the integration driver."""

    url: str
    mime_type: str


@dataclass
class AssistantError:
    """Error detail for a failed assistant processing attempt."""

    code: AssistantErrorCode
    message: str


AssistantEventData: TypeAlias = (
    AssistantSttResponse
    | AssistantTextResponse
    | AssistantSpeechResponse
    | AssistantError
)


@dataclass
class AssistantEvent:
    """Assistant event payload sent via the ``assistant_event`` message.

    This payload is emitted by the integration driver to start the audio stream and
    to provide optional feedback about voice command processing and outcome.
    """

    type: AssistantEventType
    entity_id: str
    session_id: int
    data: AssistantEventData | None = None


class MediaContentType(str, Enum):
    """Media content types for media browsing."""

    ALBUM = "album"
    APP = "app"
    APPS = "apps"
    ARTIST = "artist"
    CHANNEL = "channel"
    CHANNELS = "channels"
    COMPOSER = "composer"
    EPISODE = "episode"
    GAME = "game"
    GENRE = "genre"
    IMAGE = "image"
    MOVIE = "movie"
    MUSIC = "music"
    PLAYLIST = "playlist"
    PODCAST = "podcast"
    RADIO = "radio"
    SEASON = "season"
    TRACK = "track"
    TV_SHOW = "tv_show"
    URL = "url"
    VIDEO = "video"


class MediaClass(str, Enum):
    """Media classes for media browsing."""

    ALBUM = "album"
    APP = "app"
    ARTIST = "artist"
    CHANNEL = "channel"
    COMPOSER = "composer"
    DIRECTORY = "directory"
    EPISODE = "episode"
    GAME = "game"
    GENRE = "genre"
    IMAGE = "image"
    MOVIE = "movie"
    MUSIC = "music"
    PLAYLIST = "playlist"
    PODCAST = "podcast"
    SEASON = "season"
    TRACK = "track"
    TV_SHOW = "tv_show"
    URL = "url"
    VIDEO = "video"


@dataclass
class PagingOptions:
    """
    Pagination options.

    Attributes:
        page (int | None):
            Page number, 1-based.
        limit (int | None):
            Number of items returned per page.
    """

    page: int | None
    limit: int | None


@dataclass
class BrowseOptions:
    """
    Browsing media options.

    Attributes:
        media_id (str | None):
            Optional media content ID to restrict browsing.
        media_type (MediaContentType | None):
            Optional media content type to restrict browsing.
        stable_ids (bool | None):
            Hint to the integration to return stable media IDs.
        paging (PagingOptions | None):
            Optional paging object to limit returned items.
    """

    media_id: str | None
    media_type: MediaContentType | None
    stable_ids: bool | None
    paging: PagingOptions | None


@dataclass
class SearchMediaFilter:
    """
    Search media filter options.

    Attributes:
        media_classes (list[MediaClass]|None):
            Optional list of media classes to filter the results.
        artist (str|None):
            Optional artist name.
        album (str|None):
            Optional album name.
    """

    media_classes: list[MediaClass] | None
    artist: str | None
    album: str | None


@dataclass
class SearchOptions(BrowseOptions):
    """
    Browsing media request message.

    Attributes:
        query (str):
            Free text search query.
        filter (MediaContentType | None):
            Optional media content type to restrict browsing.
        stable_ids (bool | None):
            Hint to the integration to return stable media IDs.
        paging (PagingOptions | None):
            Optional paging object to limit returned items.
    """

    query: str
    filter: SearchMediaFilter | None


@dataclass
class BrowseMediaMsgData(BrowseOptions):
    """
    Browsing media request message.

    Attributes:
        entity_id (str):
            media-player entity ID to browse.
    """

    entity_id: str


@dataclass
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
    filter: SearchMediaFilter | None


@dataclass
class BrowseMediaItem:
    """Browse Media Item object."""

    title: str
    media_class: str
    media_type: str
    media_id: str
    can_browse: bool = field(default=False)
    can_play: bool = field(default=False)
    can_search: bool = field(default=False)
    subtitle: str | None = field(default=None)
    artist: str | None = field(default=None)
    album: str | None = field(default=None)
    thumbnail: str | None = field(default=None)
    duration: int | None = field(default=None)
    items: list["BrowseMediaItem"] | None = field(default=None)

    def __post_init__(self):
        """Apply default values on missing fields."""
        for attribute in fields(self):
            if (
                not isinstance(attribute.default, dataclasses.MISSING.__class__)
                and getattr(self, attribute.name) is None
            ):
                setattr(self, attribute.name, attribute.default)


@dataclass
class BrowseResults:
    """
    Browsing media results.

    Attributes:
        media (BrowseMediaItem | None):
            The browsed media item, or `undefined` if not found.
        paging (PagingOptions):
            Pagination metadata for this result page.
    """

    media: BrowseMediaItem | None
    paging: PagingOptions


@dataclass
class SearchResults:
    """
    Browsing media results.

    Attributes:
        media (list[BrowseMediaItem]):
            Array of matching media items. Pass an empty array if no results were found.
        paging (PagingOptions):
            Pagination metadata for this result page.
    """

    media: list[BrowseMediaItem]
    paging: PagingOptions
