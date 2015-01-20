from struct import Struct
from datetime import datetime


class Measurement:

    def __init__(self):
        self.id_ = None
        self.stamp = None
        self.Irms = None
        self.Vrms = None
        self.Phase = None

    def get_server(self):
        return self.id_, self.Vrms, self.Irms

    def get_mcu(self):
        return self.id_, self.Irms, self.Vrms, self.Phase

    def set(self, id_, Irms, Vrms, Phase):
        self.id_ = id_
        self.Irms = Irms
        self.Vrms = Vrms
        self.Phase = Phase

    def __str__(self):
        return "ID %d, Vrms %d, Irms %d" % (self.id_, self.Vrms, self.Irms)


class MCUComm:

    def __init__(self):
        """
        One circuit is defined as a string containing 5 fields
        | id_ (16 bits) | Irmd (16) | Vrms (16) | Phase (16) |
        """
        self.pkg = Struct("hhhh")

    def unpack(self, string):
        m = Measurement()
        m.set(*self.pkg.unpack(string))
        return m

    def pack(self, measurement):
        return self.pkg.pack(*measurement.get_mcu())

    def read(self, cmd):
        a = reduce(lambda s, c: s + chr(int(c)), cmd, "")
        return self.unpack(a)


class ServerComm:

    def __init__(self, protocol=4, pivi_id=4):
        """
        We add a header with the protocol version when sending it to the cloud.
        We will not send phase for now.
        | HEADER | CIRCUIT | VOLTAGE | CURRENT | CRC |
        """
        self.prot = protocol
        self.pkg = Struct("BIHIBHHH")
        self.header_struct = Struct("BIHI")
        pivi_mac = 10000
        self.less_mac = pivi_mac + pivi_id

    def create_header(self, msg_type):
        """
        Creates the header for the PIVI measurment package.
        | Protocol | LESS MAC | MSG TYPE | TIMESTAMP |
        """
        t = self.create_timestamp()
        return (self.prot, self.less_mac, msg_type, t)

    def create_timestamp(self):
        """
        Creates a timestamp representation according to the LESS Protocol v4
        spec.
        """
        now = datetime.now()
        year = (now.year - 2000) << 27
        month = now.month << 22
        day = now.day << 17
        hour = now.hour << 12
        minute = now.minute << 6
        second = now.second

        timestamp = year + month + day + hour + minute + second
        return timestamp

    def _crc16(self, crc, byte):
        """
        Calculates crc16-ibm of a message.

        :param crc: CRC calculated in previous iteration.
                    For the first one it should be 0xFFFF.
        :param byte: New byte to calculate the CRC.
        :returns: Current CRC.
        """
        crc ^= byte
        for i in range(0, 8):
            if crc & 1:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc = (crc >> 1)
        return crc

    def calc_crc16(self, msg):
        msg_int = [ord(c) for c in msg]
        crc = 0xFFFF
        for byte in msg_int[:-2]:
            self._crc16(crc, byte)

        return crc

    def pack(self, measurement):
        id_, V, I = measurement.get_server()
        h = self.create_header(1001)
        p = list(h)
        p.append(id_)
        p.append(V)
        p.append(I)
        p.append(0)
        msg = self.pkg.pack(*p)
        crc = self.calc_crc16(msg)
        p[-1] = crc
        return self.pkg.pack(*p)

    def unpack(self, server_string):
        m = Measurement()
        a = self.pkg.unpack(server_string)
        m.set(a[4], a[6], a[5], 0)
        return m
