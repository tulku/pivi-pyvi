# This file is part of the Pyvi software package. Released
# under the Creative Commons ATT-NC-ShareAlire license
# http://creativecommons.org/licenses/by-nc-sa/4.0/
# Copyright (C) 2014, 2015 LESS Industries S.A.
# Lucas Chiesa <lucas@lessinduestries.com>


from transport import Transport
from serial import Serial


class SerialTransport(Transport):
    """
    This transports the messages over a Serial Port.
    """
    def __init__(self):
        Transport.__init__(self)
        self.port = None
        self.baudrate = None

    def _open(self):
        self.serial = Serial(**self.settings)

    def read(self):
        return self.serial.read(size=1)

    def flush(self):
        self.serial.flush()
