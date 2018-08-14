import socket, argparse, binascii

# Usage:
# python2.7 sync_word2.py -ip localhost -port 7000 -syncWord 0x5B53575D -packetLength 4

parser = argparse.ArgumentParser()
parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-port', type=long, required =True) # Port number
parser.add_argument ('-syncWord',required=True) #Entry to the sync word
parser.add_argument ('-packetLength', type=int, required=True) #Payload size
args = parser.parse_args() 

# Check if sync word is in appropriated ascii hexadecimal representation
if args.syncWord[:2] != '0x':
  print "-syncWord should be in the format hexadecimal format. Ex: '0x5B53575D'"
  print 'Exiting...'
  exit()
if (len(args.syncWord)%2) != 0:
  print "-syncWord length should be even! Two ascii chars representing each byte. Ex: '0x5B53575D'"
  print 'Exiting...'
  exit()

# Store the sync word as a decimal value
syncWord = int(args.syncWord,16)
syncWord_len = (len(args.syncWord)/2)-1
syncWord_bin = bin(syncWord)
print 'Seeking input stream for sync word:', hex(syncWord) ,'- Length:',syncWord_len,'bytes - Decimal:', syncWord ,'- Binary:', syncWord_bin


print 'Connecting to', args.ip, args.port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket
client_socket.connect((args.ip, args.port)) #Connects the client to the server


def readByte():
  inputByte_str = client_socket.recv(1)
  if not inputByte_str:
    print 'Connection Lost!'
    client_socket.close()
    exit()
  else:
    print 'readByte():', hex(ord(inputByte_str)), bin(ord(inputByte_str)), inputByte_str 
    return ord(inputByte_str)


# fill the comparison buffer with the syncWord size
inputBuffer = 0
for n in range(syncWord_len):
  inputByte = readByte()
  inputBuffer = (inputBuffer<<8)+inputByte
  
# print hex(inputBuffer), inputBuffer, bin(inputBuffer), type(inputBuffer)

## TODO: unfinished filtering


client_socket.close()

