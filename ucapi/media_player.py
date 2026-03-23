"""
Media-player entity definitions.

:copyright: (c) 2023 by Unfolded Circle ApS.
:license: MPL-2.0, see LICENSE for more details.
"""

import logging
from enum import Enum, StrEnum
from typing import Any

from .api_definitions import (
    BrowseOptions,
    BrowseResults,
    CommandHandler,
    SearchOptions,
    SearchResults,
    StatusCodes,
)
from .entity import Entity, EntityTypes

_LOG = logging.getLogger(__name__)


class States(str, Enum):
    """Media-player entity states."""

    UNAVAILABLE = "UNAVAILABLE"
    UNKNOWN = "UNKNOWN"
    ON = "ON"
    OFF = "OFF"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"
    STANDBY = "STANDBY"
    BUFFERING = "BUFFERING"


class Features(str, Enum):
    """Media-player entity features."""

    ON_OFF = "on_off"
    TOGGLE = "toggle"
    VOLUME = "volume"
    VOLUME_UP_DOWN = "volume_up_down"
    MUTE_TOGGLE = "mute_toggle"
    MUTE = "mute"
    UNMUTE = "unmute"
    PLAY_PAUSE = "play_pause"
    STOP = "stop"
    NEXT = "next"
    PREVIOUS = "previous"
    FAST_FORWARD = "fast_forward"
    REWIND = "rewind"
    REPEAT = "repeat"
    SHUFFLE = "shuffle"
    SEEK = "seek"
    MEDIA_DURATION = "media_duration"
    MEDIA_POSITION = "media_position"
    MEDIA_TITLE = "media_title"
    MEDIA_ARTIST = "media_artist"
    MEDIA_ALBUM = "media_album"
    MEDIA_IMAGE_URL = "media_image_url"
    MEDIA_TYPE = "media_type"
    DPAD = "dpad"
    """Directional pad navigation provides cursor_up, _down, _left, _right, _enter commands."""
    NUMPAD = "numpad"
    """Number pad, provides digit_0 .. digit_9 commands."""
    HOME = "home"
    """Home navigation support with home and back commands."""
    MENU = "menu"
    """Menu navigation support with menu and back commands."""
    CONTEXT_MENU = "context_menu"
    """Context menu (for example, right-clicking or long pressing an item)."""
    GUIDE = "guide"
    """Program guide support with guide and back commands."""
    INFO = "info"
    """Information popup / menu support with info and back commands."""
    COLOR_BUTTONS = "color_buttons"
    """Color button support for function_red, _green, _yellow, _blue commands."""
    CHANNEL_SWITCHER = "channel_switcher"
    """Channel zapping support with channel_up and _down commands."""
    SELECT_SOURCE = "select_source"
    """Media playback sources or inputs can be selected."""
    SELECT_SOUND_MODE = "select_sound_mode"
    """Sound modes can be selected, e.g., stereo or surround."""
    EJECT = "eject"
    """The media can be ejected, e.g., a slot-in CD or USB stick."""
    OPEN_CLOSE = "open_close"
    """The player supports opening and closing, e.g., a disc tray."""
    AUDIO_TRACK = "audio_track"
    """The player supports selecting or switching the audio track."""
    SUBTITLE = "subtitle"
    """The player supports selecting or switching subtitles."""
    RECORD = "record"
    """The player has recording capabilities with record, my_recordings, live commands."""
    SETTINGS = "settings"
    """The player supports a settings menu."""
    PLAY_MEDIA = "play_media"
    """The player supports playing a specific media item."""
    CLEAR_PLAYLIST = "clear_playlist"
    """The player allows clearing the active playlist."""
    BROWSE_MEDIA = "browse_media"
    """The player supports browsing media containers."""
    SEARCH_MEDIA = "search_media"
    """The player supports searching for media items."""
    SEARCH_MEDIA_CLASSES = "search_media_classes"
    """The player provides a list of media classes as filter for searches."""
    PLAY_MEDIA_ACTION = "play_media_action"
    """The player supports the play_media action parameter to either play or enqueue."""


class Attributes(str, Enum):
    """Media-player entity attributes."""

    STATE = "state"
    VOLUME = "volume"
    MUTED = "muted"
    MEDIA_DURATION = "media_duration"
    MEDIA_POSITION = "media_position"
    MEDIA_POSITION_UPDATED_AT = "media_position_updated_at"
    MEDIA_TYPE = "media_type"
    MEDIA_IMAGE_URL = "media_image_url"
    MEDIA_TITLE = "media_title"
    MEDIA_ARTIST = "media_artist"
    MEDIA_ALBUM = "media_album"
    REPEAT = "repeat"
    SHUFFLE = "shuffle"
    SOURCE = "source"
    SOURCE_LIST = "source_list"
    SOUND_MODE = "sound_mode"
    SOUND_MODE_LIST = "sound_mode_list"
    MEDIA_ID = "media_id"
    MEDIA_PLAYLIST = "media_playlist"
    PLAY_MEDIA_ACTION = "play_media_action"
    SEARCH_MEDIA_CLASSES = "search_media_classes"


class Commands(str, Enum):
    """Media-player entity commands."""

    ON = "on"
    OFF = "off"
    TOGGLE = "toggle"
    PLAY_PAUSE = "play_pause"
    STOP = "stop"
    PREVIOUS = "previous"
    NEXT = "next"
    FAST_FORWARD = "fast_forward"
    REWIND = "rewind"
    SEEK = "seek"
    VOLUME = "volume"
    VOLUME_UP = "volume_up"
    VOLUME_DOWN = "volume_down"
    MUTE_TOGGLE = "mute_toggle"
    MUTE = "mute"
    UNMUTE = "unmute"
    REPEAT = "repeat"
    SHUFFLE = "shuffle"
    CHANNEL_UP = "channel_up"
    CHANNEL_DOWN = "channel_down"
    CURSOR_UP = "cursor_up"
    """Directional pad up"""
    CURSOR_DOWN = "cursor_down"
    """Directional pad down"""
    CURSOR_LEFT = "cursor_left"
    """Directional pad left"""
    CURSOR_RIGHT = "cursor_right"
    """Directional pad right"""
    CURSOR_ENTER = "cursor_enter"
    """Directional pad enter"""
    DIGIT_0 = "digit_0"
    DIGIT_1 = "digit_1"
    DIGIT_2 = "digit_2"
    DIGIT_3 = "digit_3"
    DIGIT_4 = "digit_4"
    DIGIT_5 = "digit_5"
    DIGIT_6 = "digit_6"
    DIGIT_7 = "digit_7"
    DIGIT_8 = "digit_8"
    DIGIT_9 = "digit_9"
    FUNCTION_RED = "function_red"
    FUNCTION_GREEN = "function_green"
    FUNCTION_YELLOW = "function_yellow"
    FUNCTION_BLUE = "function_blue"
    HOME = "home"
    """Home menu"""
    MENU = "menu"
    """General menu"""
    CONTEXT_MENU = "context_menu"
    """Context menu"""
    GUIDE = "guide"
    """Program guide menu."""
    INFO = "info"
    """Information menu / what's playing."""
    BACK = "back"
    """Back / exit function for menu navigation."""
    SELECT_SOURCE = "select_source"
    """Select media playback source or input from the available sources."""
    SELECT_SOUND_MODE = "select_sound_mode"
    """Select a sound mode from the available modes."""
    RECORD = "record"
    """Start, stop or open recording menu (device dependant)."""
    MY_RECORDINGS = "my_recordings"
    """Open recordings."""
    LIVE = "live"
    """Switch to live view."""
    EJECT = "eject"
    """Eject media."""
    OPEN_CLOSE = "open_close"
    """Open or close."""
    AUDIO_TRACK = "audio_track"
    """Switch or select audio track."""
    SUBTITLE = "subtitle"
    """Switch or select subtitle."""
    SETTINGS = "settings"
    """Settings menu"""
    SEARCH = "search"
    PLAY_MEDIA = "play_media"
    """Play or enqueue a media item."""
    CLEAR_PLAYLIST = "clear_playlist"
    """Remove all items from the playback queue. Current playback behavior is integration-dependent (keep playing the current item or clearing everything)."""


class DeviceClasses(str, Enum):
    """Media-player entity device classes."""

    RECEIVER = "receiver"
    SET_TOP_BOX = "set_top_box"
    SPEAKER = "speaker"
    STREAMING_BOX = "streaming_box"
    TV = "tv"


class Options(str, Enum):
    """Media-player entity options."""

    SIMPLE_COMMANDS = "simple_commands"
    VOLUME_STEPS = "volume_steps"


class MediaType(str, Enum):
    """Media types."""

    MUSIC = "MUSIC"
    RADIO = "RADIO"
    TVSHOW = "TVSHOW"
    MOVIE = "MOVIE"
    VIDEO = "VIDEO"


class RepeatMode(str, Enum):
    """Repeat modes."""

    OFF = "OFF"
    ALL = "ALL"
    ONE = "ONE"


class MediaPlayAction(StrEnum):
    """Media Play actions."""

    PLAY_NOW = "PLAY_NOW"
    PLAY_NEXT = "PLAY_NEXT"
    ADD_TO_QUEUE = "ADD_TO_QUEUE"


class MediaPlayer(Entity):
    """
    Media-player entity class.

    See https://github.com/unfoldedcircle/core-api/blob/main/doc/entities/entity_media_player.md
    for more information.
    """

    # pylint: disable=R0917
    def __init__(
        self,
        identifier: str,
        name: str | dict[str, str],
        features: list[Features],
        attributes: dict[str, Any],
        device_class: DeviceClasses | None = None,
        options: dict[str, Any] | None = None,
        area: str | None = None,
        cmd_handler: CommandHandler = None,
    ):
        """
        Create media-player entity instance.

        :param identifier: entity identifier
        :param name: friendly name
        :param features: media-player features
        :param attributes: media-player attributes
        :param device_class: optional media-player device class
        :param options: options
        :param area: optional area
        :param cmd_handler: handler for entity commands
        """
        super().__init__(
            identifier,
            name,
            EntityTypes.MEDIA_PLAYER,
            features,
            attributes,
            device_class=device_class,
            options=options,
            area=area,
            cmd_handler=cmd_handler,
        )

    async def browse(self, options: BrowseOptions) -> BrowseResults | StatusCodes:
        """
        Execute entity browsing request.

        Returns NOT_IMPLEMENTED if no handler is installed.

        :param options: browsing parameters
        :return: browsing response or status code if any error occurs
        """
        _LOG.warning(
            "Media browsing not supported for %s. Request: %s",
            self.id,
            options,
        )
        return StatusCodes.NOT_IMPLEMENTED

    async def search(self, options: SearchOptions) -> SearchResults | StatusCodes:
        """
        Execute media search request.

        Returns NOT_IMPLEMENTED if no handler is installed.

        :param options: search parameters
        :return: search response or status code if any error occurs
        """
        _LOG.warning(
            "Media searching not supported for %s. Request: %s",
            self.id,
            options,
        )
        return StatusCodes.NOT_IMPLEMENTED
