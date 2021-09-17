import socket
import sys
import socket
import sys
import time
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('192.168.0.3', 10000)
print('connecting to {} port {}'.format(*server_address))
sock.connect(server_address)

try:

	# Send data
	message = b'Hola loser'
	print('sending {!r}'.format(message))
	sock.send(message)

	
	data = sock.recv(1024)
	print('received {!r}'.format(data))
	
finally:
	print('closing socket')
	sock.close()