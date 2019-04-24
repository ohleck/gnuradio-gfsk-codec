from bitarray import bitarray
from comm_utils import AX25Packet, add_stuffing

# Description:
# This script generates a binary file with sample packets to send to AX5043 radio. The packets are in HDLC frame format.

PREAMBLE = b'\xFF'*200
POSTAMBLE = b'\x55'*200
FLAG = b'\x7E'
FILE_PATH = '/tmp/tx_data.bin' # Path to write the binary data

f = open(FILE_PATH, 'wb')

# for i in range(100):
#     p1 = [x for x in range(31)]
#     p1.append(i)
#     payload_data = bytes(p1)
#     hdlc_packet = assemble_hdlc_packet(PREAMBLE, FLAG, payload_data)
#     packet = assemble_raw_packet(payload_data)
#     print(packet)
    # f.write(hdlc_packet)

payload = b'FX6FRA\xe0F4KJX\x00\xe1\x03\xf0\x05\x0bgE#\x01\x11\x06t'
payload_barr = bitarray()
payload_barr.frombytes(payload)
payload_barr_stuffed = add_stuffing(payload_barr.to01())
payload_stuffed_bytes = bitarray(payload_barr_stuffed)
packet = PREAMBLE + FLAG + payload_stuffed_bytes.tobytes() + FLAG + POSTAMBLE
print(packet)
f.write(packet)
f.close()