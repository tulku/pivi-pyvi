# This file is part of the Pyvi software package. Released
# under the Creative Commons ATT-NC-ShareAlire license
# http://creativecommons.org/licenses/by-nc-sa/4.0/
# Copyright (C) 2014, 2015 LESS Industries S.A.
# Lucas Chiesa <lucas@lessinduestries.com>


from pyvi import ServerComm
from pyvi import MCUComm
from pyvi import Measurement

from pyvi import TestTransport

import unittest


class MCUCommTest(unittest.TestCase):

    def setUp(self):
        self.c = MCUComm()
        self.m = Measurement()

        self.m.set(1, 15, 220, 0)

    def test_set(self):
        pkg = self.c.pack(self.m)
        t = self.c.unpack(pkg)
        self.assertEqual(self.m.id_, t.id_)
        self.assertEqual(self.m.Irms, t.Irms)


class ServerCommTest(unittest.TestCase):

    def setUp(self):
        self.s = ServerComm(pivi_id=0)
        self.m = Measurement()
        self.mac = self.s.less_mac
        self.m.set(1, 15, 220, 0)

    def test_set(self):
        pkg = self.s.pack(self.m)
        t = self.s.unpack(pkg)
        self.assertEqual(self.mac*10+self.m.id_, t.id_)
        self.assertAlmostEqual(self.m.Irms, t.Irms, 5)


class TransportTest(unittest.TestCase):

    def setUp(self):
        self.t = TestTransport()

    def test_read_byte(self):
        self.t._ans('j')
        self.assertEqual('j', self.t.read())

    def test_read_full_mcu_pkg(self):
        self.t._ans("\x7E\xAA\x55\x7F")
        pkg = self.t.read_package_from_xmega()
        self.assertEqual((0xAA, 0x55), tuple(pkg))

    def test_timeout_mcu_pkg(self):
        # the package is missing the end pkg character.
        self.t._ans("\x7E\xAA\x55\x00\x00")
        pkg = self.t.read_package_from_xmega()
        self.assertIsNone(pkg)

    def test_stuffed_full_mcu_pkg(self):
        self.t._ans("\x7E\x7D\x8A\x45\x7F")
        pkg = self.t.read_package_from_xmega()
        self.assertEqual((0xAA, 0x45), tuple(pkg))

    def test_encode_no_stuff(self):
        a = self.t.encode_for_xmega("\x41\x42")
        self.assertEquals("".join(a), "\x7E\x41\x42\x7F")

    def test_encode_with_stuff(self):
        a = self.t.encode_for_xmega("\x41\x7F\x42")
        self.assertEquals("".join(a), "\x7E\x41\x7D\x5F\x42\x7F")

    def test_autogen(self):
        c = MCUComm()
        auto_t = TestTransport(True)
        pkg = auto_t.read_package_from_xmega()
        m = c.read(pkg)
        self.assertTrue(m.id_ in [1, 2, 3, 4, 5, 6])


if __name__ == '__main__':
    unittest.main()
