class Transport:
    """
    This is an abstract class which defines the interface that
    a transport object should have.
    """

    def __init__(self):
        self.settings = {}

    def _to_string(self, cmd):
        """
        Transforms a list of integers into a string.

        :param cmd: command to send.
        :type cmd: int list
        :returns: the string representing the command.
        :rtype: string
        """
        return reduce(lambda s, c: s + chr(int(c)), cmd, "")

    def _to_int_list(self, cmd_string):
        """
        Transforms a received string to a list of integers.

        :param cmd_string: the string-encoded command.
        :type cmd_string: string
        :returns: A integer list holding the commando.
        :rtype: int list
        """
        return [ord(c) for c in cmd_string]

    def _open(self):
        """
        Actual method that opens the communication channel
        using the setted parameters.
        """
        raise NotImplementedError("Not implemented.")

    def open(self, settings):
        """ Open the communication channel. """
        self.settings = settings
        return self._open()

    def write(self, value):
        """
        Write a value to the channel.

        :param value: The data to send.
        :type value: int
        """
        raise NotImplementedError("Not implemented.")

    def read(self):
        """
        Write a value to the channel.

        :return: The data read.
        :rtype: int
        """
        raise NotImplementedError("Not implemented.")

    def flush(self):
        """
        Deletes the input and output buffers.
        """
        raise NotImplementedError("Not implemented.")

    def print_pkg(self, pkg):
        return str(pkg)

    def calc_crc16(self, crc, byte):
        return 0

    def encode_for_xmega(self, pkg):
        """
        Sends a package to the xmega.
        """
        reserved = ['\x7E', '\x7F', '\x7D']
        encoded = ['\x7E']
        for byte in pkg:
            if byte in reserved:
                encoded.append('\x7D')
                encoded.append(chr(ord(byte) ^ 0x20))
            else:
                encoded.append(byte)

        encoded.append('\x7F')
        return encoded

    def read_package_from_xmega(self):
        """
        Receives a full package from the measurement shield.
        This function blocks the execution until a full package is read or a
        time out is reached.

        :returns: A list of integers that form the package. The CRC is already
            stripped. None if CRC error or Timeout.
        """
        pack_start = False
        byte_stuff = False
        keep_reading = True
        timeout = False
        crc = 0xFFFF
        package = []

        while (keep_reading):
            byte = self.read()
            if byte == '':
                # Timeout on reading
                timeout = True
                keep_reading = False
            elif byte == '\x7E':
                # Package start byte
                pack_start = True
                package = []
            elif byte == '\x7F':
                # Package end byte
                if pack_start is False:
                    # We did not read start byte first.
                    continue
                else:
                    # We read the entire package.
                    keep_reading = False
            elif byte == '\x7D':
                # Byte stuffing: the next one needs XOR
                byte_stuff = True
            elif pack_start is True:
                if byte_stuff is False:
                    # Un-stuffed byte
                    b = ord(byte)
                else:
                    # Stuffed byte
                    b = ord(byte) ^ 0x20
                    byte_stuff = False
                package.append(b)
                crc = self.calc_crc16(crc, b)
        # We stopped reading...
        if timeout is True:
            #print "Error: Timeout reading - PC << " + str(package)
            return None
        elif crc != 0:
            #print "Error: CRC error - PC << " + self.print_pkg(package)
            return None
        else:
            #print "PC << " + self.print_pkg(package[0:-2])
            return package
