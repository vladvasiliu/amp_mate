from unittest import TestCase

from amp_mate.simulators.rotel_simulator import RA1572


class TestRA1572Power(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_wrong_state(self):
        with self.assertRaises(ValueError):
            self.amp.power = 'something'

    def test_returns_standby_or_on(self):
        return_dict = {True: "on",
                       False: "standby"}

        for value in return_dict:
            with self.subTest(value=value):
                self.amp._power = value
                self.assertEqual(self.amp.power, return_dict[value])


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
