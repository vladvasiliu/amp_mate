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

    def test_volume_is_set(self):
        # volume = 0 is illegal
        for vol in range (self.amp.VOL_MIN+1, self.amp.VOL_MAX + 1):
            with self.subTest(value=vol):
                self.amp.volume = str(vol)
                self.assertEqual(self.amp.volume, "%02i" % vol)


class TestRA1572Mute(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()
        self.mute_dict = {True: 'on',
                          False: 'off'}

    def test_raises_for_wrong_state(self):
        with self.assertRaises(ValueError):
            self.amp.mute = 'something'

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


class TestRA1572AutoUpdate(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_wrong_state(self):
        with self.assertRaises(ValueError):
            self.amp.auto_update = 'something'

    def test_on_off(self):
        update_dict = {True: 'on',
                       False: 'off'}
        for state in update_dict.items():
            with self.subTest(value=state[1]):
                self.amp.auto_update = state[1]
                self.assertIs(self.amp._auto_update, state[0])

    def test_returns_auto_or_manual(self):
        update_dict = {True: 'auto',
                       False: 'manual'}
        for value in update_dict.items():
            with self.subTest(value=value[1]):
                self.amp._auto_update = value[0]
                self.assertEqual(self.amp.auto_update, value[1])


class TestRA1572Source(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_wrong_source(self):
        with self.assertRaises(ValueError):
            self.amp.source = 'toto'

    def test_sets_the_source(self):
        for src in self.amp.SOURCES:
            with self.subTest(value=src):
                self.amp.source = src
                self.assertEqual(self.amp.source, src)


class TestRA1572Command(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_wrong_command(self):
        self.assertRaises(ValueError, self.amp.command, 'toto')

    def test_returns_string_if_auto_update_is_on(self):
        commands = [('power', 'on'),
                    ('vol', 'up'),
                    ('mute', None),
                    ('opt1', None)]
        self.amp.auto_update = 'on'
        for value in commands:
            with self.subTest(value=value):
                result = self.amp.command(*value)
                self.assertIsInstance(result, str)

    def test_returns_none_if_auto_update_is_off(self):
        commands = [('power', 'on'),
                    ('vol', 'up'),
                    ('mute', None),
                    ('opt1', None)]
        self.amp.auto_update = 'off'
        for value in commands:
            with self.subTest(value=value):
                result = self.amp.command(*value)
                self.assertIsNone(result)


class TestRA1572Request(TestCase):
    def setUp(self) -> None:
        self.amp = RA1572()

    def test_raises_for_wrong_command(self):
        self.assertRaises(ValueError, self.amp.request, 'toto')
