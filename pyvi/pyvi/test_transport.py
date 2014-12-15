from transport import Transport


class TestTransport(Transport):
    """
    This is a fake transport used only during the UnitTests.
    Uses a string to store the sent message and can generate
    answers.
    """
    def __init__(self):
        Transport.__init__(self)
        self.wrote = ""
        self.ans_buff = ""

    def _wrote(self):
        return self.wrote

    def _clean(self):
        self.wrote = ""
        self.ans_buff = ""

    def _ans(self, ans):
        self.ans_buff = ans

    def _open(self):
        return self.settings['speed']

    def write(self, value):
        self.wrote = value

    def read(self, size=1):
        read = self.ans_buff[:size]
        self.ans_buff = self.ans_buff[size:]
        return read

    def flush(self):
        pass
