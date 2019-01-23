import struct
from utils.tcp_utils import TCPClient


def text_to_int_arr(text):
    int_arr = []
    for s in text:
        int_arr.append(ord(s))

    return int_arr


def int_arr_to_text(int_arr):
    text = []
    for i in int_arr:
        text += chr(i)

    return ''.join(text)


text = 'sometextgoeshere'
text = '***************************************************************ZZZZZZZZ' + \
    text  # preambule of datastring
text += 'UUUUUUUU'  # postambule of datastring

int_arr = text_to_int_arr(text)
int_arr_length = len(int_arr)
# print(int_arr)

byte_arr = []
struct_str = 'B' * int_arr_length
byte_arr = struct.pack('@'+struct_str, *int_arr)

# for n in range(0, int(len(varicode_string)/8)):
# 	f.write(struct.pack('@B', u8))

client = TCPClient('localhost', 7000)
# Connect to TCP server
connected = client.connect()
# Check if connected
if connected:
    print('Connection Successful')
    # Create a dummy message with two integers (ii) and pack them as bytes
    msg = struct.pack('>ii', 10, 100)
    # Send bytes to TCP server
    while True:
        sent = client.send_data(byte_arr)
        # Print if sent

client.disconnect()
