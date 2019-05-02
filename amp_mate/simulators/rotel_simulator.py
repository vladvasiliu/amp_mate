from typing import Optional


class RA1572:
    """Simulates a Rotel RA-1572 v2.65 and newer amplifier. Not all functions are implemented.

    Command codes are based on the RS232/IP Protocol.
    Source: http://www.rotel.com/sites/default/files/product/rs232/RA1572%20Protocol.pdf
    """
    VOL_MIN = 0
    VOL_MAX = 96
    TONE_MIN = 0
    TONE_MAX = 10
    BAL_MIN = -15
    BAL_MAX = 15
    DIM_MIN = 0
    DIM_MAX = 6
    INPUTS = ["cd", "aux", "tuner", "phono", "bal_xlr",
              "coax1", "coax2", "opt1", "opt2", "usb", "bluetooth", "pcusb"]

    def __init__(self):
        self._power = True
        self._input = "cd"
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
    def mute(self, value:Optional[str]=None):
        """Set mute state. If value is None, toggle mute."""
        if value is 'on':
            self._mute = True
        elif value is 'off':
            self._mute = False
        elif value is None:
            self._mute = not self._mute
        else:
            raise ValueError('Unknown mute state %s' % value)
