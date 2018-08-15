from __future__ import print_function
import socket, sys, argparse, os, binascii, struct



# creation of a custom print function that writes do stderr

def eprint(msg, *args, **kwargs):
    print_function(msg, file=sys.stderr, *args, **kwargs)

stdout = os.fdopen(sys.stdout.fileno(), 'wb', 0)

parser = argparse.ArgumentParser()

parser.add_argument ('-syncword',required=True)#Entry to the sync word
parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-payload', type=int, required=True) #Payload size
parser.add_argument ('-port', type=long, required =True) # Port number
args = parser.parse_args() 

sync_word_list= list(args.syncword)
sync_word_list.append("")

bits_list = list()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket

client_socket.connect((args.ip, args.port)) #Connects the client to the server

length_sync = len(sync_word_list) -1


i = 0



while True:

	data = client_socket.recv(2)

	if not data:

		stdout.write('\n\nConnection Lost\n')
		break

	else:

		bits = bytearray(data) 
		bits_hex = binascii.b2a_hex(bits) #conversion to hexa (bit 1 == 01 and bit 0 == 00)
		list_bit_hex = list(bits_hex) #creating a list to separate it
		bits_comp = list_bit_hex[len(bits_hex)-1:] # deleting the first bit (bit 1 == 1, bit 0 == 0)

		if (i < length_sync) and (bits_comp[0] == sync_word_list[i]) : #comparing each element --> not working

			bits_list.append(bits_comp[0]) #adding bits to an array
			i = i + 1
			bits = bytearray(2)
			bits_hex = ''
			bits_comp = list()

		elif (i >= length_sync) and (i < (length_sync + args.payload)): #allowing payload

			bits_list.append(bits_comp[0]) #Creating a list with the elements
			i = i +1
			bits = bytearray(2)
			bits_hex = ''
			bits_comp = list()

		elif i == (length_sync + args.payload): #printing output

			bits_out = ''.join(bits_list) #Creating a string to print ---> not working
			stdout.write(bits_out)
			stdout.write('\n printed output\n')
			bits_out = list()
			bits_list = list() #restarting the list
			i = 0
			bits = bytearray(2)
			bits_hex = ''
			bits_comp = list()

		else:

			i=0
			bits = bytearray(2)
			bits_hex = ''
			bits_comp = list()

client_socket.close()

##TODO -> Add hexadecimal conversion for input and output