from unittest import TestCase

from amp_mate.simulators.rotel_simulator import RA1572


class TestRA1572Power(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_wrong_state(self):
        with self.assertRaises(ValueError):
            self.amp.power = 'something'

    def test_on_off(self):
        power_dict = {True: "on",
                      False: "off"}
        for state in power_dict.items():
            with self.subTest(value=state[1]):
                self.amp.power = state[1]
                self.assertIs(self.amp._power, state[0])

    def test_toggle(self):
        power_dict = {True: "on",
                      False: "standby"}
        for state in power_dict.items():
            with self.subTest(value=state[1]):
                self.amp._power = not state[0]
                self.amp.power = 'toggle'
                self.assertEqual(self.amp.power, state[1])

    def test_returns_standby_or_on(self):
        power_dict = {True: "on",
                      False: "standby"}
        for value in power_dict:
            with self.subTest(value=value):
                self.amp._power = value
                self.assertEqual(self.amp.power, power_dict[value])


class TestRA1572Volume(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_out_of_range(self):
        for value in [-1, 0, 97, 100]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.amp.volume = value

    def test_min_is_0(self):
        self.amp._volume = 123
        self.amp.volume = 'min'
        self.assertEqual(self.amp._volume, 0)

    def test_vol_up_doesnt_overshoot(self):
        self.amp._volume = self.amp.VOL_MAX
        self.amp.volume = 'up'
        self.assertEqual(self.amp._volume, self.amp.VOL_MAX)

    def test_vol_dwn_doesnt_overshoot(self):
        self.amp._volume = self.amp.VOL_MIN
        self.amp.volume = 'dwn'
        self.assertEqual(self.amp._volume, self.amp.VOL_MIN)

    def test_number_is_zero_padded(self):
        for value in [0, 2, 20]:
            with self.subTest(value=value):
                self.amp._volume = value
                self.assertEqual(self.amp.volume, "%02i" % value)


class TestRA1572Mute(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()
        self.mute_dict = {True: 'on',
                          False: 'off'}

    def test_raises_for_wrong_state(self):
        with self.assertRaises(ValueError):
            self.amp.power = 'something'

    def test_on_off(self):
        for state in self.mute_dict.items():
            with self.subTest(value=state[1]):
                self.amp.mute = state[1]
                self.assertIs(self.amp._mute, state[0])

    def test_returns_on_or_off(self):
        for value in self.mute_dict.items():
            with self.subTest(value=value[1]):
                self.amp._mute = value[0]
                self.assertEqual(self.amp.mute, value[1])

    def test_toggle(self):
        for value in self.mute_dict.items():
            with self.subTest(value=value[1]):
                self.amp._mute = not value[0]
                self.amp.mute = None
                self.assertEqual(self.amp.mute, value[1])
