from pyvi import ServerComm
from pyvi import MCUComm
from pyvi import Measurement

from pyvi import TestTransport

import unittest


class MCUCommTest(unittest.TestCase):

    def setUp(self):
        self.c = MCUComm()
        self.m = Measurement()

        self.m.set(1, 10, 15, 220, 0)

    def test_set(self):
        pkg = self.c.pack(self.m)
        t = self.c.unpack(pkg)
        self.assertEqual(self.m.id_, t.id_)
        self.assertEqual(self.m.Irms, t.Irms)


class ServerCommTest(unittest.TestCase):

    def setUp(self):
        self.s = ServerComm()
        self.m = Measurement()

        self.m.set(1, 10, 15, 220, 0)

    def test_set(self):
        pkg = self.s.pack(self.m)
        t = self.s.unpack(pkg)
        self.assertEqual(self.m.id_, t.id_)
        self.assertEqual(self.m.Irms, t.Irms)


class TransportTest(unittest.TestCase):

    def setUp(self):
        self.t = TestTransport()

    def test_read_byte(self):
        self.t._ans('j')
        self.assertEqual('j', self.t.read())

    def test_read_full_mcu_pkg(self):
        self.t._ans("\x7E\xAA\x55\x00\x00\x7F")
        pkg = self.t.read_package_from_xmega()
        self.assertEqual((0xAA, 0x55), tuple(pkg))

    def test_timeout_mcu_pkg(self):
        # the package is missing the end pkg character.
        self.t._ans("\x7E\xAA\x55\x00\x00")
        pkg = self.t.read_package_from_xmega()
        self.assertIsNone(pkg)

    def test_stuffed_full_mcu_pkg(self):
        self.t._ans("\x7E\x7D\x8A\x45\x00\x00\x7F")
        pkg = self.t.read_package_from_xmega()
        self.assertEqual((0xAA, 0x45), tuple(pkg))


if __name__ == '__main__':
    unittest.main()
