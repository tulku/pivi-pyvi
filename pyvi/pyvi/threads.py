import threading
import Queue

from pyvi import MCUComm
from pyvi import ServerComm


class ThreadSerial(threading.Thread):

    def __init__(self, logger, transport, queue):
        """
        Threads that read from the Serial port and saves data to a Queue.
        """
        super(ThreadSerial, self).__init__()
        self.port = transport
        self.protocol = MCUComm()
        self.running = False
        self.l = logger
        self.queue = queue

    def run(self):
        self.running = True
        while(self.running):
            try:
                pkg = self.port.read_package_from_xmega()
                if pkg is not None:
                    m = self.protocol.read(pkg)
                    if not self.queue.full():
                        self.queue.put(m, timeout=0.1)
                        msg = "Read: {}".format(m)
                        self.l.debug(msg)
            except:
                self.l.exception("Exception while reading from serial.")

    def kill(self):
        self.running = False


class ThreadUdp(threading.Thread):

    def __init__(self, logger, transport, pivi_id, queue):
        """
        Thread that reads from a Queue and sends data to a remote server
        """
        super(ThreadUdp, self).__init__()

        self.protocol = ServerComm(pivi_id=pivi_id)
        self.port = transport
        self.mac = self.protocol.less_mac
        self.running = False
        self.l = logger
        self.queue = queue

    def run(self):
        self.running = True
        while(self.running):
            try:
                m = self.queue.get(timeout=1)
            except Queue.Empty:
                self.l.debug("Incoming queue empty")
                continue
            try:
                if m is not None:
                    msg = "Sending from mac: {}, pkg: {}".format(self.mac, m)
                    self.l.debug(msg)
                    pkg = self.protocol.pack(m)
                    self.port.write(pkg)
            except:
                self.l.exception("Exception while sending via UDP.")

    def kill(self):
        self.running = False
