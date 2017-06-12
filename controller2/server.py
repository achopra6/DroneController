import socket 
import sys
import os
import time

import code
import readline
import rlcompleter

sys.path.append('../src')

from Bybop_Discovery import *
import Bybop_Device

print 'Searching for devices'

discovery = Discovery([DeviceID.BEBOP_DRONE])

discovery.wait_for_change()

devices = discovery.get_devices()

discovery.stop()

if not devices:
    print 'Oops ...'
    sys.exit(1)

device = devices.itervalues().next()

print 'Will connect to ' + get_name(device)

d2c_port = 54321
controller_type = "PC"
controller_name = "bybop shell"

drone = Bybop_Device.create_and_connect(device, d2c_port, controller_type, controller_name)

if drone is None:
    print 'Unable to connect to a product'
    sys.exit(1)

vars = globals().copy()
vars.update(locals())
readline.set_completer(rlcompleter.Completer(vars).complete)
readline.parse_and_bind("tab: complete")
shell = code.InteractiveConsole(vars)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 6000)
print >>sys.stderr, 'Starting up on %s port %s' % server_address
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print >>sys.stderr, 'waiting for a connection'
    connection, client_address = sock.accept()
    try:
        print >>sys.stderr, 'connection from', client_address
        welcome = 'You are connected to Bebop Drone\n t: Take-Off\n l: Land\n e: Emergency'
        connection.sendall(welcome)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(1)
            print >>sys.stderr, 'Received "%s"' % data
            if data == 't':
                drone.take_off()
                message = 'Taking Off'
            if data == 'l':
                drone.land()
                message = 'Landing'
            if data == 'e':
                drone.emergency()
                message = 'Emergency Landing'
            if data == 'w':
                drone.send_data('ARDrone3','Piloting','PCMD',True,0,20,0,0,0)
                message = 'Pitch to +20'
            if data == 's':
               	drone.send_data('ARDrone3','Piloting','PCMD',True,0,-20,0,0,0)
                message = 'Pitch to -20'
            if data == 'r':
                drone.send_data('ARDrone3','Piloting','PCMD',True,20,0,0,0,0)
                message = 'Roll to +20'
            if data == 'f':
                drone.send_data('ARDrone3','Piloting','PCMD',True,-20,0,0,0,0)
                message = 'Roll to -20'
            if data == 'y':
                drone.send_data('ARDrone3','Piloting','PCMD',True,0,0,0,20,0)
                message = 'Gaz to 20'
            if data == 'h':
                drone.send_data('ARDrone3','Piloting','PCMD',True,0,0,0,-20,0)
                message = 'Gaz to -20'
            if data == 'i':
                drone.send_data('ARDrone3','Piloting','PCMD',True,0,0,20,0,0)
                message = 'Yaw to +20'
            if data == 'k':
                drone.send_data('ARDrone3','Piloting','PCMD',True,0,0,-20,0,0)
                message = 'Yaw to -20'
            if data == 'p':
                drone.send_data('ARDrone3','Piloting','PCMD',True,0,0,0,0,0)
                message = 'All to 0'
            if data == 'q':
                drone.land()
                drone.stop()
                message = 'Thanks for connecting. Stopping drone'
                connection.sendall(message)
                break
            connection.sendall(message)
            
    finally:
        # Clean up the connection
        drone.land()
        drone.stop()
        connection.close()
        sock.close()
        sys.exit()
