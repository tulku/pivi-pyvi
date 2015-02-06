from transport import Transport
from protocol import MCUComm, Measurement
import time
import random


class TestTransport(Transport):
    """
    This is a fake transport used only during the UnitTests.
    Uses a string to store the sent message and can generate
    answers.
    """
    def __init__(self, auto_gen=False):
        Transport.__init__(self)
        self.comm = MCUComm()
        self.wrote = ""
        self.ans_buff = ""
        self.auto_gen = auto_gen

    def _wrote(self):
        return self.wrote

    def _clean(self):
        self.wrote = ""
        self.ans_buff = []

    def _ans(self, ans):
        self.ans_buff = list(ans)

    def _open(self):
        return self.settings['speed']

    def _gen_message(self):
        """ Generates a fake pivi message. It stores it internally and
        when using 'read' you get it byte by byte. """
        m = Measurement()
        v = 220 + random.randint(-10, 10)
        i = 5 + random.randint(-3, 14)
        m.set(42, v*i, (i**2)**2, (v**2)**2)
        msg = self.comm.pack(m)
        self.ans_buff = self.encode_for_xmega(msg)

    def write(self, value):
        self.wrote = value

    def read(self, size=1):

        if self.auto_gen:
            if len(self.ans_buff) == 0:
                self._gen_message()

        # In case we want to force an answer for some test.
        if self.ans_buff:
            read = self.ans_buff.pop(0)
        else:
            read = ''

        return read

    def flush(self):
        pass
