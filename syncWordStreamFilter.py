#!/usr/bin/python2.7
import socket
import argparse
import datetime
import sys
from utils.tcp_utils import TCPClient
from bitarray import bitarray

# Usage:
# ./syncWordStreamFilter.py -ip localhost -port 7000 -syncWord 0x53 -packet_length 4 -display_time
#
# Optional: -verbose -display_time
# use '| more' to control the verbose output
#
# Simulation environment:
# The command bellow creates and TCP server providing the binary file as content and restarting the operation after the client disconnects.
# while true; do nc -l 127.0.0.1 7000 < samples/sampleBitstream_syncWord_0x5370.bin; done

parser = argparse.ArgumentParser()
parser.add_argument('-ip', required=True)  # IP Address
parser.add_argument('-port', type=long, required=True)  # Port number
parser.add_argument('-syncWord', required=True)  # Entry to the sync word
parser.add_argument('-packet_length', type=int, required=True)  # Payload size
parser.add_argument('-verbose', action='store_true')
parser.add_argument('-display_time', action='store_true')
args = parser.parse_args()

# Check if sync word is in appropriated ascii hexadecimal representation
if args.syncWord[:2] != '0x':
    print "-syncWord should be in the format hexadecimal format. Ex: '0x5B53575D'"
    print "Exiting..."
    exit()
if (len(args.syncWord) % 2) != 0:
    print "-syncWord length should be even! Two ascii chars representing each byte. Ex: '0x5B53575D'"
    print "Exiting..."
    exit()

# Store the sync word as a decimal value
syncWord = int(args.syncWord, 16)
syncWord_len = (len(args.syncWord)/2)-1
# syncWord_bin = bin(syncWord)
syncWord_bin = "{0:#0{1}b}".format(syncWord, 2+syncWord_len*8)
if args.verbose:
    print 'Seeking input stream for sync word:', hex(
        syncWord), '(syncWord length:', syncWord_len, 'B)', 'Binary:', syncWord_bin, 'Decimal:', syncWord


flag_bin = bitarray('01111110')

if args.verbose:
    print 'Connecting to', args.ip, args.port

client = TCPClient(args.ip, args.port)
# Connect to TCP server
connected = client.connect()
if connected:
    print('Connection Successful')


def unpacked_to_packed(byte_arr):
    binary_str = ''
    for by in byte_arr:
        binary_str += str(ord(by))

    binary = bitarray(binary_str)
    return binary.tobytes()


def readNextByte():
    inputByte_arr = client.receive_data(8)
    inputByte_str = unpacked_to_packed(inputByte_arr)
    if not inputByte_str:
        if args.verbose:
            print 'Connection Lost!'
        client.close()
        exit()
    else:
        return ord(inputByte_str)


def readByteChunk(length):
    readBuffer = []
    # loop through N single reads instead of socket buffer to avoid network delays / buffer sizes mismatches issues
    for n in range(length):
        inputByte_arr = client.receive_data(8)
        inputByte_str = unpacked_to_packed(inputByte_arr)
        a = bitarray()
        a.frombytes(inputByte_str)
        if not inputByte_str:
            if args.verbose:
                print 'Connection Lost!'
            client.close()
            exit()
        readBuffer.append(inputByte_str)
    return readBuffer


def debugPrintBuffers():
    print '\033[94m'+'bit:', (streamBytePosition*8) + \
        localBitPosition, 'Byte:', streamBytePosition,
    print '\033[92m'+'Analyzing:', "{0:#0{1}x}".format(
        comparisonBuffer, 2+syncWord_len*2), "{0:#0{1}b}".format(comparisonBuffer, 2+syncWord_len*8)[2:],
    print '\033[93m'+'<', bin(nextBit)[2], '<'+'\033[95m',
    binStr = str("{0:#0{1}b}".format(inputBuffer, 10))[2:]
    print binStr[:localBitPosition]+'\033[7m' + \
        binStr[localBitPosition]+'\033[27m'+binStr[localBitPosition+1:],
    print "{0:#0{1}x}".format(inputBuffer, 4),
    print '\033[91m'+'Matches:', matchesCount,
    if now:
        print 'Last:', now.strftime("%H:%M:%S"),
    print ''


def decode_nrzi(bin_arr):
    ref_bit = bitarray('0')
    uncoded_bin_arr = ref_bit+bin_arr
    decoded_bin_arr = bitarray('')
    for i in range(1, len(uncoded_bin_arr)):
        decoded_bin_arr.append(uncoded_bin_arr[i-1] == uncoded_bin_arr[i])

    return decoded_bin_arr


def remove_stuffing(bin_arr):
    index = bin_arr.search(bitarray('11111'))
    removed = 0
    for i in index:
        bin_arr.pop(i+5-removed)
        removed += 1

    return bin_arr


def compute_crc(tm_tf):
    """Compute the CRC-CCITT checksum.

    Keyword arguments:
    tm_tf -- Complete transfer frame [bytes]

    Outputs:
    checksum -- Computed checksum for the given bitstring [bytes]

    TODO: In line documenting

    """
    bin_string = ''
    for b in tm_tf:
        bin_string += bin(b)[2:].zfill(8)

    crc = 0xffff
    i = 0
    while(i < (len(bin_string))):
        x = 0
        for j in range(8):
            x = x << 1
            x |= 1 if (bin_string[i + j] == '1') else 0

        crc_new = ((crc >> 8) | (crc << 8)) & 0xFFFF

        crc_new ^= x
        crc_new = crc_new & 0xFFFF

        crc_new ^= (crc_new & 0xff) >> 4
        crc_new = crc_new & 0xFFFF

        crc_new ^= crc_new << 12
        crc_new = crc_new & 0xFFFF

        crc_new ^= (crc_new & 0xff) << 5
        crc_new = crc_new & 0xFFFF

        crc = crc_new
        i += 8

    crc = (~(crc & 0xFFFF) & (crc | 0xFFFF))

    crcval = format(crc & 0xFFFF, '04x')
    crcval = format(int(crcval, 16), '016b')

    crc_bytes = struct.pack('!H', int(crcval, 2))
    return crc_bytes


def check_crc(bin_arr):
    '''
    Check CRC according to crc-16-genibus:
    http://crcmod.sourceforge.net/crcmod.predefined.html
    '''
    payload_data_bin = bin_arr[:-16]  # remove CRC
    crc_bin = bin_arr[-16:]

    # payload_data_bin.reverse()

    # crc_calc = CRCCCITT(version='FFFF').calculate(payload_data_bin.tobytes())
    crc_calc = compute_crc(payload_data_bin.tobytes())

    # print('CRC RX:', int(crc_bin.to01(), 2))
    # print('CRC CALC:', int.from_bytes(crc_calc, byteorder='big'))

    return (int(crc_bin.to01(), 2) == int.from_bytes(crc_calc, byteorder='big'))
    # print('CRC CALC:', crc_calc)



# fill the comparison buffer with the syncWord size
matchesCount = 0
now = False
comparisonBuffer = 0
for n in range(syncWord_len):
    inputBuffer = (readNextByte() & 0b11111111)
    comparisonBuffer = (comparisonBuffer << 8) | inputBuffer
    if args.verbose:
        print 'inputBuffer:\t', "  {0:#0{1}b}".format(
            inputBuffer, 2+syncWord_len*8), "{0:#0{1}x}".format(inputBuffer, 2+syncWord_len*2)
    if args.verbose:
        print 'comparisonBuffer:', "{0:#0{1}b}".format(
            comparisonBuffer, 2+syncWord_len*8), "{0:#0{1}x}".format(comparisonBuffer, 2+syncWord_len*2)


streamBytePosition = 0
nextBit = 0
while True:
    # Reads the TCP source byte per byte, but analyzes locally in bit steps,
    # because syncWord is not necessarely aligned in the incoming byte sequence

    # comparisonBuffer was already filled in the previous step and is ready for comparison,
    # but still read one subsequent byte, for the following bitwise insertions in the comparison buffer
    inputBuffer = (readNextByte() & 0b11111111)

    for localBitPosition in range(8):

        inputBuffer_str = "{0:#0{1}b}".format(inputBuffer, 10)
        nextBit = int(inputBuffer_str[localBitPosition+2], 2)
        if args.verbose:
            debugPrintBuffers()

        if comparisonBuffer == syncWord:
            matchesCount = matchesCount + 1
            if args.verbose:
                print '\033[91m'+">>>", hex(
                    syncWord), 'SYNC WORD FOUND processing byte:', streamBytePosition, '- Input bit count:', (streamBytePosition*8)+localBitPosition
            packet = readByteChunk(args.packet_length+30)
            bin_arr = bitarray()
            bin_arr.frombytes(''.join(packet))
            frame_bin = decode_nrzi(bin_arr)
            print(frame_bin)
            flag_idx = frame_bin.search(flag_bin)
            packet_stuffed = frame_bin[(flag_idx[0]+len(flag_bin)):flag_idx[1]]
            packet_bin = remove_stuffing(packet_stuffed.copy())

            valid_crc = check_crc(packet_bin)
            if valid_crc:
                print('Valid CRC found!')
                # valid_packets += 1

            print hex(syncWord),
            # merge with the next byte after syncWord (inputBuffer), pre-fetched from memory
            print "{0:#0{1}x}".format(inputBuffer, 4),
            for i in range(len(packet)):
                print "{0:#0{1}x}".format(ord(packet[i]), 4),
            now = datetime.datetime.now()
            if args.display_time:
                print "\tReceived at:", now,
            print ""
            streamBytePosition = streamBytePosition + syncWord_len + args.packet_length

        # Moving comparisonBuffer to the next bit:
        comparisonBuffer = ((comparisonBuffer << 1) &
                            int('1'*8*syncWord_len, 2)) | nextBit

    streamBytePosition = streamBytePosition + 1
    sys.stdout.flush()


if args.verbose:
    print "syncWordStreamFilter.py end! Closing TCP connection..."
client.close()
