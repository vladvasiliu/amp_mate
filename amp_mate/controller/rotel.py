import asyncio
from asyncio import AbstractEventLoop
from enum import Enum
from typing import Iterable, Optional


class RotelStatusException(Exception):
    pass


class RotelVolumeException(RotelStatusException):
    pass


class RotelToneConfig:
    def __init__(self, bypass: bool = False, low: int = -10, high: int = 10, bands: Iterable[str] = ("bass", "treble")):
        self.bypass: bypass
        self.low = low
        self.high = high
        self.bands = bands


class RotelConfigBase:
    def __init__(
        self,
        min_volume: int,
        max_volume: int,
        sources: Iterable[str],
        speakers: Optional[Iterable[str]] = None,
        source_control: bool = False,
        tone: Optional[RotelToneConfig] = None,
        max_dimmer: Optional[int] = None,
        separator: str = "=",
        recv_end: str = "$",
        send_end: str = "!",
    ):
        self.min_volume = min_volume
        self.max_volume = max_volume
        self.sources = sources
        self.source_control = source_control
        self.speakers = speakers
        self.tone = tone
        self.max_dimmer = max_dimmer
        self.separator = separator
        self.recv_end = recv_end
        self.send_end = send_end


class RotelPower(Enum):
    ON = True
    OFF = False


class RotelStatus:
    def __init__(self, config: RotelConfigBase):
        self._config = config
        self.power: Optional[RotelPower] = None
        self.source: Optional[str] = None
        self.volume: Optional[int] = None
        self.mute: Optional[bool] = None
        self.tone_config: Optional[RotelToneConfig] = None
        self.input_frequency: Optional[int] = None
        self.speakers: Optional[Iterable[str]] = None
        self.dimmer = Optional[int] = None
        self.version: Optional[str] = None
        self.model: Optional[str] = None

    def update_status(self, amp_response: str) -> bool:
        """Updates the status from a message received from the amp and returns whether something changed."""
        param, value = response_splitter(amp_response, separator=self._config.separator, end=self._config.recv_end)
        return True

    @property
    def volume(self) -> int:
        return self._volume

    @volume.setter
    def volume(self, value: int):
        if self._volume != value:
            if self._config.min_volume <= value <= self._config.max_volume:
                self._volume = value
            else:
                raise RotelVolumeException(
                    "Volume must be between %s and %s" % (self._config.min_volume, self._config.max_volume)
                )


class RotelController:
    """Encapsulates a protocol to communicate with Rotel RS232 V2 capable amps.

    This class uses asyncio to communicate with the amp. It is NOT thread-safe!
    """

    def __init__(self, host: str, port: int, config: RotelConfigBase, loop: Optional[AbstractEventLoop] = None):
        self.host = host
        self.port = port
        self.config = config
        self._reader = self._writer = None
        self._loop = loop

    async def connect(self):
        self._reader, self._writer = await asyncio.open_connection(self.host, self.port, loop=self._loop)

    async def disconnect(self):
        self._writer.close()
        await self._writer.wait_closed()
        self._writer = self._reader = None

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.disconnect()
