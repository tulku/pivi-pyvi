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
