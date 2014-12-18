from pyvi import ServerComm
from pyvi import MCUComm
from pyvi import Measurement

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

if __name__ == '__main__':
    unittest.main()
