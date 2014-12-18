from struct import Struct


class Measurement:

    def __init__(self):
        self.id_ = None
        self.stamp = None
        self.Irms = None
        self.Vrms = None
        self.Phase = None

    def get_server(self):
        return self.id_, self.stamp, self.Irms, self.Vrms

    def get_mcu(self):
        return self.id_, self.stamp, self.Irms, self.Vrms, self.Phase

    def set(self, id_, stamp, Irms, Vrms, Phase):
        self.id_ = id_
        self.stamp = stamp
        self.Irms = Irms
        self.Vrms = Vrms
        self.Phase = Phase


class MCUComm:

    def __init__(self):
        """
        One circuit is defined as a string containing 5 fields
        | id_ (16 bits) | stamp (32) | Irmd (16) | Vrms (16) | Phase (16) |
        """
        self.pkg = Struct("hihhh")

    def unpack(self, string):
        m = Measurement()
        m.set(*self.pkg.unpack(string))
        return m

    def pack(self, measurement):
        return self.pkg.pack(*measurement.get_mcu())


class ServerComm:

    def __init__(self, protocol=4):
        """
        We add a header with the protocol version when sending it to the cloud.
        We will not send phase for now.
        | protocol (8 bits) | id_ (16) | stamp (32) | Irms (16) | Vrms (16) |
        """
        self.prot = protocol
        self.pkg = Struct("Bhihh")

    def pack(self, measurement):
        return self.pkg.pack(self.prot, *measurement.get_server())

    def unpack(self, server_string):
        m = Measurement()
        prot, id_, stamp, Irms, Vrms = self.pkg.unpack(server_string)
        m.set(id_, stamp, Irms, Vrms, 0)
        return m
