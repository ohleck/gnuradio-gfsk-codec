import socket, argparse

parser = argparse.ArgumentParser()
parser.add_argument ('-syncword',required=True)#Entry to the sync word
parser.add_argument ('-packet_length', type=int, required=True) #Payload size
parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-port', type=long, required =True) # Port number
args = parser.parse_args() 

print 'Connecting to', args.ip, args.port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket
client_socket.connect((args.ip, args.port)) #Connects the client to the server



while True:

	# print 'Trying to read...'
	data = client_socket.recv(1)

	if not data:
		print 'Connection Lost!'
		break

	else:
		print len(data)
		print type(data)
		# print data.encode('utf-8').hex()


client_socket.close()