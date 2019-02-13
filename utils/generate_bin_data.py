from bitarray import bitarray
from comm_utils import assemble_hdlc_packet

# Description:
# This script generates a binary file with sample packets to send to AX5043 radio. The packets are in HDLC frame format.

PREAMBLE = b'\xAA'*16
FLAG = b'\x7E'

f = open('/tmp/tx_data.bin', 'wb')

for i in range(100):
    p1 = [x for x in range(31)]
    p1.append(i)
    payload_data = bytes(p1)
    hdlc_packet = assemble_hdlc_packet(PREAMBLE, FLAG, payload_data)
    f.write(hdlc_packet)

f.close()
