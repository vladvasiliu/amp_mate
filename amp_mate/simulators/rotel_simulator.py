import re
from typing import Optional


class RA1572:
    """Simulates a Rotel RA-1572 v2.65 and newer amplifier. Not all functions are implemented.

    Command codes are based on the RS232/IP Protocol.
    `Source <http://www.rotel.com/sites/default/files/product/rs232/RA1572%20Protocol.pdf>`_.

    Implemented functions are in the :attr:`~_COMMANDS` and :attr:`~_REQUESTS` attributes.
    """
    VOL_MIN = 0
    VOL_MAX = 96
    TONE_MIN = 0
    TONE_MAX = 10
    BAL_MIN = -15
    BAL_MAX = 15
    DIM_MIN = 0
    DIM_MAX = 6
    _SOURCES = ["cd", "aux", "tuner", "phono", "bal_xlr",
                "coax1", "coax2", "opt1", "opt2", "usb", "bluetooth", "pcusb"]

    _COMMANDS = {'power': 'power',
                 'vol': 'volume',
                 'mute': 'mute',
                 'rs232_update': 'auto_update'
                 }
    _REQUESTS = {'power': 'power',
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

    # Commands with an argument, like `vol_up`
    MSG_PATTERNS = {re.compile(r'^%s(?:_(?P<arg>[a-z0-9\-+]+))?!$' % cmd): attr for cmd, attr in _COMMANDS.items()}
    """ This is a map of the form :code:`pattern: attribute`. Whichever pattern matches indicates witch attribute to
    get/set. 
    
    Command patterns will match with an `arg` group. This may be ``None``, e.g. in the case of ``mute!``.
    Requests match without the `arg` group.
    """
    # Commands without an argument, like `cd`
    MSG_PATTERNS.update({re.compile(r'^(?P<arg>%s)!$' % src): 'source' for src in _SOURCES})
    # Requests
    MSG_PATTERNS.update({re.compile(r'%s\?$' % req): attr for req, attr in _REQUESTS.items()})

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
        return "power=%s" % ("on" if self._power else "standby")

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
        return "volume=%02i" % self._volume

    @volume.setter
    def volume(self, value: str):
        if value == 'up':
            self._volume = min(self._volume + 1, self.VOL_MAX)
        elif value == 'dwn':
            self._volume = max(self._volume - 1, self.VOL_MIN)
        elif value == 'min':
            self._volume = self.VOL_MIN
        elif self.VOL_MIN < int(value) <= self.VOL_MAX:
            self._volume = int(value)
        else:
            raise ValueError('Unknown volume %s' % value)

    @property
    def mute(self):
        return "mute=%s" % ("on" if self._mute else "off")

    @mute.setter
    def mute(self, value: Optional[str] = None):
        """Set mute state. If value is None, toggle mute."""
        if value == 'on':
            self._mute = True
        elif value == 'off':
            self._mute = False
        elif value is None:
            self._mute = not self._mute
        else:
            raise ValueError('Unknown mute state %s' % value)

    @property
    def source(self):
        return 'source=%s' % self._source

    @source.setter
    def source(self, value: str):
        if value in self._SOURCES:
            self._source = value
        else:
            raise ValueError("Unknown source %s" % value)

    @property
    def auto_update(self) -> str:
        """ Whether the amp sends an update when the state changes.

        Values are `auto` or `manual`.
        """
        return 'update_mode=%s' % ('auto' if self._auto_update else 'manual')

    @auto_update.setter
    def auto_update(self, value: str):
        """Set auto update.

        Possible values are `on` and `off`.
        """
        if value == 'on':
            self._auto_update = True
        elif value == 'off':
            self._auto_update = False
        else:
            raise ValueError("Unknown auto update mode %s" % value)

    def handle_message(self, msg: str) -> Optional[str]:
        """Interprets the message received from the client.

        There are two types of messages:

        1. Commands, aka setters. They end with a `!`
        2. Requests, aka getters. They end with a `?`

        If the command is a getter, the function always returns something or raises an exception.
        If the command is a setter, the function only returns if :attr:`~auto_update` is `True` and if the function
        returns something.

        The command is matched with a pattern. See the description of :attr:`~MSG_PATTERNS` above for how this works.

        Attributes:
            msg (str): The message as received from the client.

        Returns:
            Optional[str]: The reply of the command.

        Raises:
            ValueError: If the message is not understood for various reasons (unknown command, wrong termination, etc).
        """
        for pattern, attr in self.MSG_PATTERNS.items():
            match = pattern.fullmatch(msg)

            if not match:
                continue

            if match.groups():
                arg, = match.groups()
                setattr(self, attr, arg)
                result = getattr(self, attr) if self._auto_update else None
            else:
                result = getattr(self, attr)
            break
        else:
            raise ValueError('Message not understood: `%s`' % msg)

        if result:
            result += "$"
            return result
