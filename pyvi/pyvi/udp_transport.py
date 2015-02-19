from transport import Transport
import socket


class UdpTransport(Transport):
    """
    This transports the messages over an UDP channel.
    We use it to send datagrams to the LESS cloud.
    """
    def __init__(self):
        Transport.__init__(self)
        self.sock = None
        self.srv_addr = None

    def _clean(self):
        self.wrote = ""
        self.ans_buff = ""

    def _ans(self, ans):
        self.ans_buff = ans

    def _open(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.svr_addr = self.settings['server']
        self.svr = self.svr_addr.split(':')[0]
        self.port = int(self.svr_addr.split(':')[1])

    def write(self, value):
        self.sock.sendto(value, (self.svr, self.port))

    def read(self):
        pass

    def flush(self):
        pass
