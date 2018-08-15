#!/usr/bin/python2.7
import socket, argparse, datetime, sys

# Usage:
# ./streamFilter.py -ip localhost -port 7000 -syncWord 0x53 -packet_length 4 -display_time
#
# Optional: -verbose | -display_time
#
# Simulation environment: 
# The command bellow creates and TCP server providing the binary file as content and restarting the operation after the client disconnects.
# while true; do nc -l 127.0.0.1 7000 < samples/sampleBitstream_syncWord_0x5370.bin; done

parser = argparse.ArgumentParser()
parser.add_argument ('-ip', required =True) # IP Address
parser.add_argument ('-port', type=long, required =True) # Port number
parser.add_argument ('-syncWord',required=True) #Entry to the sync word
parser.add_argument ('-packet_length', type=int, required=True) #Payload size
parser.add_argument ('-verbose', action='store_true')
parser.add_argument ('-display_time', action='store_true')
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
if args.verbose: print 'Seeking input stream for sync word:', hex(syncWord) ,'- Length:',syncWord_len,'bytes - Decimal:', syncWord ,'- Binary:', syncWord_bin


if args.verbose: print 'Connecting to', args.ip, args.port
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Creates the client socket
client_socket.connect((args.ip, args.port)) #Connects the client to the server


def readNextByte():
  inputByte_str = client_socket.recv(1)
  if not inputByte_str:
    if args.verbose: print 'Connection Lost!'
    client_socket.close()
    exit()
  else:
    return ord(inputByte_str)

def readByteChunk(length):
  readBuffer = []
  # loop through N single reads instead of socket buffer to avoid network dellays / buffer sizes mismatches issues
  for n in range(length):
    inputByte_str = client_socket.recv(1) 
    
    if not inputByte_str:
      if args.verbose: print 'Connection Lost!'
      client_socket.close()
      exit()

    readBuffer.append(inputByte_str)  

  return readBuffer

# fill the comparison buffer with the syncWord size
comparisonBuffer = 0
for n in range(syncWord_len):
  inputBuffer = readNextByte()
  comparisonBuffer = (comparisonBuffer<<8)+inputBuffer


streamBytePosition = 0
while True: 

  inputBuffer = readNextByte() # keeps one extra byte already in the buffer, for the next bitwise rotations

  # Rotate and analyzes locally the input stream in steps of 8 bits 
  # because the TCP source (inputBuffer) is read byte (not bit per bit)
  for localBitPosition in range(8):
    if args.verbose: print 'Processing bit:', (streamBytePosition*8)+localBitPosition, '\tcomparisonBuffer:', format(comparisonBuffer, '#010b'), "{0:#0{1}x}".format(comparisonBuffer,4), '\tStream byte:', streamBytePosition
    
    if comparisonBuffer == syncWord:
      if args.verbose: print "\nSYNC WORD",hex(syncWord),"FOUND!",'streamBytePosition:',streamBytePosition
      print hex(syncWord),
      packet = readByteChunk(args.packet_length)
      for i in range(len(packet)):
        print "{0:#0{1}x}".format( ord(packet[i]) ,4),
      
      if args.display_time: 
        print "\tReceived at:", datetime.datetime.now()
      else:
        print ""  
      sys.stdout.flush()
     
    # print "Moving comparisonBuffer to the next bit:",n
    nextBit = int( format(inputBuffer, '#010b')[localBitPosition+2] ,2) # Removes the '0b' prefix from the formating representation
    comparisonBuffer = ( comparisonBuffer<<1 & 0b11111111 ) | nextBit

  streamBytePosition = streamBytePosition + 1


if args.verbose: print "syncWordFilter.py end! Closing TCP connection..."
client_socket.close()

