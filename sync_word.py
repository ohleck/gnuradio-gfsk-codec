from __future__ import print_function
import socket, sys, argparse, os, binascii, struct



# creation of a custom print function that writes do stderr

def eprint(msg, *args, **kwargs):
    print_function(msg, file=sys.stderr, *args, **kwargs)

stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

parser = argparse.ArgumentParser()

parser.add_argument ('-syncword', required=True)#Entry to the sync word
parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-payload', type=int, required=True) #Payload size
parser.add_argument ('-port', type=long, required =True) # Port number
args = parser.parse_args() 

sync_word_list = list(args.syncword)
bits_out = list()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket

client_socket.connect((args.ip, args.port)) #Connects the client to the server

length_sync = len(sync_word_list)
i = 0

while True:
	data = client_socket.recv(10000)
	if not data:
		stdout.write('\n\nConnection Lost\n')
		break
	bits = bytearray(data)
	bits_comp = binascii.b2a_hex(bits)
	if (bits_comp == sync_word_list[i]) and (i < length_sync): #comparing each element
		bits_out.append(str(bits_comp))
		i = i + 1
	elif (i >= length_sync) and (i < (len(sync_word_list) + args.payload)): #allowing payload
		bits_out.append(str(bits_comp))
		i = i +1
	else: #printing all
		stdout.write("".join(bits_out))
		stdout.write('\n printed\n')
		bits_out = list() #deletign all the lit
client_socket.close()

##TODO -> Add hexadecimal conversion for input and output

