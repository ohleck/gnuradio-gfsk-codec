import struct
from bitarray import bitarray
from comm_utils import assemble_hdlc_packet


preambule = b'\xAA'*600
header = b'\x7E'

f = open('/tmp/tx_data.bin', 'wb')

for i in range(100):
    p1 = [x for x in range(31)]
    p1.append(i)
    payload_data = bytes(p1)
    hdlc_packet = assemble_hdlc_packet(preambule, header, payload_data)
    f.write(hdlc_packet)


# preambule = '01111110'*8
# data = '00110011'*32
# postambule = '11101110'*2

# simple_packet_bin = preambule + data + postambule
# simple_packet = bitarray(simple_packet_bin)
# # open file to write bytes
# f.write(simple_packet.tobytes())

# for n in range(0, int(len(varicode_string)/8)):
# 	f.write(struct.pack('@B', u8))

f.close()
