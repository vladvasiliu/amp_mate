import logging
from asyncio import Event
from enum import Enum, auto
from typing import Optional


logger = logging.getLogger(__name__)


class ControllerException(Exception):
    pass


class ControllerStatusException(ControllerException):
    pass


class VolumeStatus:
    """Holds volume related information.

    Attributes can be None if they're not yet known
    """

    MIN = 0
    MAX = 100

    def __init__(self):
        self._value = None
        self._mute = None
        self.changed = Event()

    @property
    def value(self) -> Optional[int]:
        return self._value

    @value.setter
    def value(self, value: int):
        if self.MIN <= value <= self.MAX:
            if value != self._value:
                self._value = value
                self.changed.set()
        else:
            message = 'Got invalid volume "%s". Should be between %s and %s.' % (value, self.MIN, self.MAX)
            logger.warning(message)
            raise ValueError(message)

    @property
    def mute(self) -> Optional[bool]:
        return self._mute

    @mute.setter
    def mute(self, value):
        if self._mute != value:
            self._mute = value
            self.changed.set()


class PlaybackState(Enum):
    PLAYING = auto()
    PAUSED = auto()
    STOPPED = auto()
    ERROR = auto()


class PlaybackStatus:
    def __init__(self, state: PlaybackState):
        self.state = state


class ControllerStatus:
    """Holds last known status of the controller

    This should only be modified by the controller
    """
    def __init__(self,
                 volume: Optional[VolumeStatus] = None,
                 playback: Optional[PlaybackStatus] = None):
        self.volume = volume
        self.playback = playback


class Controller:
    """This is an interface to control remote devices, such as Amp or Player. It uses asyncio.

    Numeric values are normalised: 0 is min, 100 is max.
    Implementation should handle conversion

    The controller is asynchronous,
    so it's not possible to return the exact status of the device at the time of the function call.
    The implementation should probably manage some sort of internal "cache" / last known good status.

    Volume goes from min = 0 to max = 100
    """
    async def __aenter__(self):
        raise NotImplementedError

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError

    async def get_volume(self) -> int:
        raise NotImplementedError

    async def set_volume(self, value: int):
        raise NotImplementedError

    async def get_mute(self) -> bool:
        raise NotImplementedError

    async def set_mute(self):
        raise NotImplementedError

    async def set_unmute(self):
        raise NotImplementedError
