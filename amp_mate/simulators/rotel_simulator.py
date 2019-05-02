import re
from typing import Optional


class RA1572:
    """Simulates a Rotel RA-1572 v2.65 and newer amplifier. Not all functions are implemented.

    Command codes are based on the RS232/IP Protocol.
    Source: http://www.rotel.com/sites/default/files/product/rs232/RA1572%20Protocol.pdf

    Implemented functions are in the COMMANDS and REQUESTS attributes.
    """
    VOL_MIN = 0
    VOL_MAX = 96
    TONE_MIN = 0
    TONE_MAX = 10
    BAL_MIN = -15
    BAL_MAX = 15
    DIM_MIN = 0
    DIM_MAX = 6
    SOURCES = ["cd", "aux", "tuner", "phono", "bal_xlr",
               "coax1", "coax2", "opt1", "opt2", "usb", "bluetooth", "pcusb"]

    COMMANDS = {'power': 'power',
                'vol': 'volume',
                'mute': 'mute',
                'rs232_update': 'auto_update'
                }
    REQUESTS = {'power': 'power',
                'source': 'source',
                'volume': 'volume',
                'mute': 'mute',
                'bypass': 'bypass',
                'bass': 'bass',
                'treble': 'treble',
                'balance': 'balance',
                'freq': 'freq',
                'speaker': 'speaker',
                'dimmer': 'dimmer',
                'version': 'version',
                'model': 'model'}

    def __init__(self):
        self._power = True
        self._source = "cd"
        self._volume = 0
        self._mute = False
        self._bypass = True
        self._bass = 0
        self._treble = 0
        self._balance = 0   # -15 = Full left / +15 = Full right
        self._speaker_a = True
        self._speaker_b = True
        self._dimmer = 0
        self._auto_update = False

    @property
    def power(self):
        return "on" if self._power else "standby"

    @power.setter
    def power(self, value: str):
        if value == 'on':
            self._power = True
        elif value == 'off':
            self._power = False
        elif value == 'toggle':
            self._power = not self._power
        else:
            raise ValueError('Unknown power mode %s' % value)

    @property
    def volume(self):
        return "%02i" % self._volume

    @volume.setter
    def volume(self, value: str):
        if value is 'up':
            self._volume = min(self._volume + 1, self.VOL_MAX)
        elif value is 'dwn':
            self._volume = max(self._volume - 1, self.VOL_MIN)
        elif value is 'min':
            self._volume = self.VOL_MIN
        elif self.VOL_MIN < int(value) <= self.VOL_MAX:
            self._volume = int(value)
        else:
            raise ValueError('Unknown volume %s' % value)

    @property
    def mute(self):
        return "on" if self._mute else "off"

    @mute.setter
    def mute(self, value: Optional[str] = None):
        """Set mute state. If value is None, toggle mute."""
        if value is 'on':
            self._mute = True
        elif value is 'off':
            self._mute = False
        elif value is None:
            self._mute = not self._mute
        else:
            raise ValueError('Unknown mute state %s' % value)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, value: str):
        if value in self.SOURCES:
            self._source = value
        else:
            raise ValueError("Unknown source %s" % value)

    @property
    def auto_update(self):
        return 'auto' if self._auto_update else 'manual'

    @auto_update.setter
    def auto_update(self, value: str):
        if value is 'on':
            self._auto_update = True
        elif value is 'off':
            self._auto_update = False
        else:
            raise ValueError("Unknown auto update mode %s" % value)

    def command(self, cmd: str, arg: Optional[str] = None) -> Optional[str]:
        try:
            prop = self.COMMANDS[cmd]
        except KeyError:
            raise ValueError('Unknown command %s' % cmd)
        setattr(self, prop, arg)
        if self._auto_update:
            return getattr(self, prop)

    def request(self, req: str) -> str:
        try:
            prop = self.REQUESTS[req]
        except KeyError:
            raise ValueError('Unknown request %s' % req)
        return getattr(self, prop)

    def handle_message(self, msg: str) -> Optional[str]:
        """Interprets the message received from the client.

        There are two types of messages:
        1. Commands, aka setters. They end with a `!`
        2. Requests, aka getters. They end with a `?`

        If the command is a getter, the function always returns something or raises an exception.
        If the command is a setter, the function only returns if auto_update is True and if the function returns
        something.
        """
        pattern = re.compile(r'^(?:(?P<command>[a-z0-9]+)(?:_(?P<arg>[a-z0-9\-+]+))?!)|(?:(?P<request>[a-z]+)\?)$')
        match = pattern.fullmatch(msg)
        if not match:
            raise ValueError('Message not understood: `%s`' % msg)
        cmd, arg, req = match.groups()

        if cmd:
            return self.command(cmd, arg)
        elif req:
            return self.request(req)
        else:
            raise ValueError('Message not understood: `%s`' % msg)
