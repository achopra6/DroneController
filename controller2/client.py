import socket
import sys
import getch

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 6000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)
try:
    
    # Send data
    #message = 'This'
    #print >>sys.stderr, 'sending "%s"' % message
    
    data = sock.recv(100)
    print '"%s"' % data
    while 1:
        char = getch.getch()
        if char == 'q': 
            break
        sock.sendall(char)
        data = sock.recv(100)
        print '%s' % data

finally:
    print >>sys.stderr, 'closing socket'
    sock.close()
    sys.exit()