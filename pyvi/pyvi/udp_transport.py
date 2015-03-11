# This file is part of the Pyvi software package. Released
# under the Creative Commons ATT-NC-ShareAlire license
# http://creativecommons.org/licenses/by-nc-sa/4.0/
# Copyright (C) 2014, 2015 LESS Industries S.A.
# Lucas Chiesa <lucas@lessinduestries.com>


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
        self.svr = self.settings['address']
        self.port = int(self.settings['port'])
        return self.reopen()

    def write(self, value):
        try:
            self.sock.sendto(value, (self.svr, self.port))
        except socket.error:
            raise
            return False
        return True

    def close(self):
        if self.sock is not None:
            print 'closing port'
            self.sock.shutdown(socket.SHUT_RDWR)
            self.sock.close()
            self.sock = None
        else:
            print 'not closing port'

    def reopen(self):
        if self.sock is None:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            except socket.error:
                print 'Failed to open udp port'
                raise
                return False
        else:
            print 'not reopening udp port'
