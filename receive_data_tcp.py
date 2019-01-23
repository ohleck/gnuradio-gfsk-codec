import struct
import re
import numpy as np
from utils.tcp_utils import TCPClient


def int_to_8bin(i):
    b = bin(i)[2:].zfill(8)
    return b


def to_text(bin_arr):
    int_arr = []
    for b in bin_arr:
        int_arr.append(int(b, 2))

    text = []
    for i in int_arr:
        text += chr(i)

    return ''.join(text)


def byte_to_str_arr(byte_arr):
    bin_arr = ''
    for by in byte_arr:
        bin_arr += str(by)

    return bin_arr


def find_preambule(bin_str_arr):
    start_idx = np.array([m.start()
                          for m in re.finditer(preambule, bin_str_arr)])
    return start_idx


def find_postambule(bin_str_arr):
    end_idx = np.array([m.start()
                        for m in re.finditer(postambule, bin_str_arr)])
    return end_idx


def extract_data(bin_str_arr):
    start_idx = find_preambule(bin_str_arr)
    end_idx = find_postambule(bin_str_arr)

    frame_bin_arr = []
    packets = 0
    correct_packets = 0
    for i in range(len(start_idx)):
        # print(bin_arr[st:st+64])
        frame = bin_str_arr[start_idx[i]:end_idx[i]]
        frame_bin = [frame[i:i+8] for i in range(0, len(frame), 8)]
        frame_bin_arr.append(frame_bin)
        txt = to_text(frame_bin)
        if txt == 'ZZZZZZZZsometextgoeshereUUUUUUUU':
            correct_packets += 1
            print(txt)
        packets += 1

    if packets:
        print('Packets found:', packets)
        
    return


preambule_number_bin = int_to_8bin(90)  # Z
preambule = preambule_number_bin * 8
# print(preambule)

postambule_number_bin = int_to_8bin(85)  # U
postambule = postambule_number_bin * 8
# print(postambule)

client = TCPClient('localhost', 5000)
# Connect to TCP server
connected = client.connect()
# Check if connected
if connected:
    print('Connection Successful')
    while True:
        # Get server response
        resp = client.receive_data()
        # Print server response
        resp_str = byte_to_str_arr(resp)
        # print(resp_str)
        extract_data(resp_str)


# print('Correct packets found:', correct_packets)
# print('%  of Correct packets found:', 100*(correct_packets/packets))
