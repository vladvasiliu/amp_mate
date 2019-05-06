from unittest import TestCase
from unittest.mock import patch

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
                self.assertEqual(self.amp._power, state[0])

    def test_toggle(self):
        power_dict = {True: "power=on",
                      False: "power=standby"}
        for state in power_dict.items():
            with self.subTest(value=state[1]):
                self.amp._power = not state[0]
                self.amp.power = 'toggle'
                self.assertEqual(self.amp.power, state[1])

    def test_returns_standby_or_on(self):
        power_dict = {True: "power=on",
                      False: "power=standby"}
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
                self.assertEqual(self.amp.volume, "volume=%02i" % value)

    def test_volume_is_set(self):
        # volume = 0 is illegal
        for vol in range (self.amp.VOL_MIN+1, self.amp.VOL_MAX + 1):
            with self.subTest(value=vol):
                self.amp.volume = str(vol)
                self.assertEqual(self.amp.volume, "volume=%02i" % vol)


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
                self.assertEqual(self.amp._mute, state[0])

    def test_returns_on_or_off(self):
        for value in self.mute_dict.items():
            with self.subTest(value=value[1]):
                self.amp._mute = value[0]
                self.assertEqual(self.amp.mute, "mute=%s" % value[1])

    def test_toggle(self):
        for value in self.mute_dict.items():
            with self.subTest(value=value[1]):
                self.amp._mute = not value[0]
                self.amp.mute = None
                self.assertEqual(self.amp.mute, "mute=%s" % value[1])


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
                self.assertEqual(self.amp._auto_update, state[0])

    def test_returns_auto_or_manual(self):
        update_dict = {True: 'auto',
                       False: 'manual'}
        for value in update_dict.items():
            with self.subTest(value=value[1]):
                self.amp._auto_update = value[0]
                self.assertEqual(self.amp.auto_update, "update_mode=%s" % value[1])


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
                self.assertEqual(self.amp.source, "source=%s" % src)


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
                regex = r'^[a-z_]+=[a-z0-9_]+$'
                self.assertRegex(result, regex)

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

    def test_returns_proper_regex(self):
        commands = ['power',
                    'volume',
                    'mute',
                    'source']
        self.amp.auto_update = 'on'
        for value in commands:
            with self.subTest(value=value):
                result = self.amp.request(value)
                regex = r'^[a-z_]+=[a-z0-9_]+$'
                self.assertRegex(result, regex)


class TestRA1572HandleMessage(TestCase):
    def setUp(self) -> None:
        self.amp=RA1572()

    def test_calls_command(self):
        with patch.object(self.amp, 'command', autospec=True) as command:
            self.amp.handle_message('vol_up!')
            command.assert_called()

    def test_calls_request(self):
        with patch.object(self.amp, 'request', autospec=True) as command:
            self.amp.handle_message('volume?')
            command.assert_called()

    def test_raises_for_invalid_message(self):
        messages = ['', 'toto', '1234?', 'toto.toto', '?', '!']
        for msg in messages:
            with self.subTest(value=msg):
                self.assertRaises(ValueError, self.amp.handle_message, msg)

    def test_answer_ends_with_dollar(self):
        result = self.amp.handle_message('volume?')
        self.assertRegex(result, r'.+\$$')

    def test_command_with_two_underscores(self):
        with patch.object(self.amp, 'command', autospec=True) as command:
            self.amp.handle_message('rs232_update_on!')
            command.assert_called_with('auto_update', 'on')
