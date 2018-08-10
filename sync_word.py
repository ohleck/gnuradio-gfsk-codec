from __future__ import print_function
import socket, sys, argparse, os, binascii, struct



# creation of a custom print function that writes do stderr

def eprint(msg, *args, **kwargs):
    print_function(msg, file=sys.stderr, *args, **kwargs)

stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

parser = argparse.ArgumentParser()

parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-port', type=long, required =True) # Port number
args = parser.parse_args() 


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket

client_socket.connect((args.ip, args.port)) #Connects the client to the server


while True:
	data = client_socket.recv(10000)
	if not data:
		stdout.write('\n\nConnection Lost\n')
		break
	bits = bytearray(data)
	bits_out = test = binascii.hexlify(bits)
	stdout.write(bits_out)

client_socket.close()