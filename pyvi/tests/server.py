import socket
import sys
from pyvi import ServerComm

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
server_address = ('localhost', 9000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

comm = ServerComm()

while True:
    data, address = sock.recvfrom(4096)
    m = comm.unpack(data)
    print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
    print >>sys.stderr, m
