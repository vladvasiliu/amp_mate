import unittest

from amp_mate.controller import VolumeStatus


class TestVolumeStatus(unittest.TestCase):
    def test_raises_for_out_of_range_values(self):
        vs = VolumeStatus()
        for value in [-1, 101, 100.1]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                vs.value = value

    def test_value_is_rounded_to_int(self):
        vs = VolumeStatus()
        for value in [0, 100, 2.2, 3.9]:
            with self.subTest(value=value):
                vs.value = value
                self.assertEqual(vs.value, round(value))
                self.assertIsInstance(vs.value, int)

    def test_changed_is_not_set_when_value_not_changed(self):
        vs = VolumeStatus()
        vs.value = 20
        vs.changed.clear()
        vs.value = 20
        self.assertFalse(vs.changed.is_set())

    def test_changed_is_set_when_value_changed(self):
        vs = VolumeStatus()
        vs.value = 20
        vs.changed.clear()
        vs.value = 21
        self.assertTrue(vs.changed.is_set())

    def test_returns_none_if_not_set(self):
        vs = VolumeStatus()
        self.assertIsNone(vs.value)
        self.assertIsNone(vs.mute)

    def test_is_not_changed_when_value_not_set(self):
        vs = VolumeStatus()
        self.assertFalse(vs.changed.is_set())

    def test_changed_is_not_set_when_mute_not_changed(self):
        vs = VolumeStatus()
        for value in [True, False]:
            with self.subTest(value=value):
                vs.mute = value
                self.assertTrue(vs.changed.is_set())


if __name__ == '__main__':
    unittest.main()
