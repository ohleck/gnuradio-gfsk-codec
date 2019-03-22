from bitarray import bitarray
from comm_utils import remove_stuffing, decode_nrzi, check_crc, AX25Packet

# Description:
# This script loads a binary file and tries to decode the data packets.
#
# Usage:
# Set the correct FLAG field in HEX. Set the correct path to where the binary file is.
#

FLAG = b'\x7E'
FILE_PATH = '/tmp/rx_data.bin' # Path to read the binary data from

# open file to read bytes
f = open(FILE_PATH, 'rb')
byte_arr = f.read()
f.close()

# Convert bytes into binary string
bin_arr_raw_str = ''
for by in byte_arr:
    bin_arr_raw_str += str(by)
bin_arr = bitarray(bin_arr_raw_str)

# Convert FLAG bytes into bits
flag_bin = bitarray()
flag_bin.frombytes(FLAG)

# Find occurrences of FLAG 
flag_idxs = bin_arr.search(flag_bin)

# Extract frames from bin stream
received_packets = 0 # Counter for received packet
valid_packets = 0 # Counter for packets with valid CRC
for i in range(len(flag_idxs)-1):
    # Sweeps through the FLAG occurences to check if it's a valid packet 

    idx = flag_idxs[i]
    next_idx = flag_idxs[i+1]

    # Remove data from two consecutive FLAGS (frame)
    frame_bin_stuffed = bin_arr[idx+len(flag_bin):next_idx]

    # Work around FLAGS found too close to another
    if len(frame_bin_stuffed) < 200:
        continue

    # Remove stuffing from frames
    packet_bin = remove_stuffing(frame_bin_stuffed)

    ax25_packet = AX25Packet(packet_bin)
    
    if (ax25_packet.header.dest_address == b'ABCDEF') & \
        (ax25_packet.header.source_address == b'UVWXYZ'):
        received_packets += 1

    # Check if it's a valid CRC packet
    if ax25_packet.valid:
        print('Valid CRC found!')
        valid_packets += 1

    
    # print(packet_barr.tobytes())

print('Received Packets found:', received_packets)
print('Valid Packets found:', valid_packets)
