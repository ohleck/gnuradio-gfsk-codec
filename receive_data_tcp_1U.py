import struct
from utils.tcp_utils import TCPClient
import threading
from time import sleep
from queue import Queue
from bitarray import bitarray
from utils.comm_utils import remove_stuffing, decode_nrzi, check_crc, AX25Packet
import sys

IP = 'localhost'
PORT = 7000

FROM_FILE = False

FILE_PATH = '/tmp/rx_data.bin' # Path to read the binary data from
FILE_PATH_TX = '/tmp/tx_data.bin' # Path to read the binary data from

CC1020_ISR_STATE_INIT = 1
CC1020_ISR_STATE_WAIT_1ST_FLAG = 2
CC1020_ISR_STATE_READ_DATA = 3
CC1020_ISR_STATE_UNSTUF = 4
CC1020_ISR_STATE_WAIT_2ND_FLAG = 5
CC1020_ISR_STATE_DELIVER_PACKET = 6

packet_queue = Queue(maxsize=5)
bit_queue = Queue(maxsize=2048)
data_counter = 0 #  used for sweeping input data file, if used

class ProcessThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self._please_stop = False

        self.taskState = CC1020_ISR_STATE_INIT
        self.ax_counter = 0
        self.frameIndex = 0
        self.rx_buffer = b''
        self.bit_counter = 0
        self.byte = 0 
        self._bit_slide_counter = 8
        self._byte_counter = 0
        self._tcp_byte = 0

        if not FROM_FILE: 
            self.connect_to_server()
            
    def run(self):
        while(1):
            # if not bit_queue.empty():
            #     bit = bit_queue.get()
            if self.receive_task(270):
                # print("Enqueued packet")
                # print(self.rx_buffer.hex())
                packet_queue.put(self.rx_buffer)
                self.rx_buffer = b''

    def stop(self):
        self._please_stop = True

    def receive_bit(self):
        if self._bit_slide_counter == 8:
            if FROM_FILE:
                global data_counter
                if data_counter == file_data_length:
                    self.stop()
                    return

                self._tcp_byte = bytes([file_data[data_counter]])
                data_counter += 1
            else:
                self._tcp_byte= self.client.receive_data(1)

            self._bit_slide_counter = 0

        out_bit = 0
        if ord(self._tcp_byte) & (0x80 >> self._bit_slide_counter): out_bit = 1
        
        self._bit_slide_counter += 1

        return out_bit

    def connect_to_server(self):
        self.client = TCPClient(IP, PORT)
        # Connect to TCP server
        connected = self.client.connect()
        if connected:
            print('Connection Successful')
            # self.client.receive_data() # read all data to flush buffers
        else:
            print('Failed to connect')

    def receive_task(self, max_length):
        if self.taskState == CC1020_ISR_STATE_INIT: # Init all variable for a new RX Process
            #  timerClearTimeoutFlag(&timerFlagTimeout)
            self.byte = 0x00
            self.bit_counter = 0
            self.frameIndex = 0
            self.ax_counter = 0
            self.rx_buffer = b''
            self.taskState = CC1020_ISR_STATE_WAIT_1ST_FLAG
            return 0

        elif self.taskState == CC1020_ISR_STATE_WAIT_1ST_FLAG: # Wait for 0x7E Flag
            #  timerClearTimeoutFlag(&timerFlagTimeout)
            in_bit = self.receive_bit()
            # print(in_bit, end = '')
            self.byte = (self.byte << 1) & 0xFF
            if (in_bit == 0):
                self.byte = self.byte & ~(0x01)
            else:
                self.byte = self.byte | 0x01 

            if (self.byte == 0x7E):
                self.taskState = CC1020_ISR_STATE_READ_DATA
                self.rx_buffer = b''

            return 0

        elif self.taskState == CC1020_ISR_STATE_READ_DATA: # Get bistream bit after bit
            in_bit = self.receive_bit()
            self.bit_counter += 1
            self.byte = (self.byte << 1) & 0xFF

            if (in_bit):
                self.byte |= 0x01
                self.ax_counter += 1
                # if received 5 consecutives '1', go to "CC1020_ISR_STATE_UNSTUF" state
                if (self.ax_counter == 5):
                    self.ax_counter = 0
                    self.taskState = CC1020_ISR_STATE_UNSTUF
                    return 0

            else:
                self.byte &= ~(0x01)
                self.ax_counter = 0

            if (self.bit_counter == 8):
                self.bit_counter = 0
                if (self.frameIndex < max_length):
                    # print(self.byte)
                    self.rx_buffer += bytes([self.byte])
                    self.frameIndex += 1
                    self.byte = 0
                else:
                    self.taskState = CC1020_ISR_STATE_WAIT_1ST_FLAG
                    self.frameIndex = 0
                    self.ax_counter = 0

            return 0

        elif self.taskState == CC1020_ISR_STATE_UNSTUF:
            in_bit = self.receive_bit()
            if (in_bit):
                # if the received bit is a '1', it can be either a FLAG or an ABORT
                self.taskState = CC1020_ISR_STATE_WAIT_2ND_FLAG
            else:
                # Unstuffing '0' by dropping next bit 0
                self.taskState = CC1020_ISR_STATE_READ_DATA
            return 0

        elif self.taskState == CC1020_ISR_STATE_WAIT_2ND_FLAG:
            in_bit = self.receive_bit()
            if (in_bit):
                # if the received bit is a '1', it's an ABORT or ERROR
                self.taskState = CC1020_ISR_STATE_INIT
                return 0
            else:
                # if the received bit is a '0', it's a FLAG
                self.taskState = CC1020_ISR_STATE_DELIVER_PACKET
                return 0

        elif self.taskState == CC1020_ISR_STATE_DELIVER_PACKET:
            #  Deliver full self.frameIndex and go back to DATA RX
            #  Since the flag might be the start of another packet
            self.taskState = CC1020_ISR_STATE_READ_DATA
            #  reset local variables
            self.byte = 0x00
            self.bit_counter = 0
            #  save value of frame index to be returned
            #  reset self.frameIndex
            self.frameIndex = 0
            return 1

        else:
            self.taskState = CC1020_ISR_STATE_INIT
            return 0

        return 0


class TMThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
        self.received_packets = 0
        self.received_address_packets = 0
        self.valid_packets = 0

    def run(self):
        while(1):
            if not packet_queue.empty():
                self.received_packets += 1
                # print("Dequeued packet: ", self.received_packets)
                packet = packet_queue.get()

                packet_bin_arr = bitarray()
                packet_bin_arr.frombytes(packet)

                if len(packet_bin_arr) < 20:
                    continue

                ax25_packet = AX25Packet(packet_bin_arr.to01())

                # Check if it's a valid CRC packet
                if ax25_packet.valid:
                    print('Valid CRC found!')
                    self.valid_packets += 1
                    print("Raw Packet:")
                    print(packet.hex())


if __name__ == "__main__":
    print("starting")

    if FROM_FILE:
        # open file to read bytes
        # f = open(FILE_PATH, 'rb')
        # file_data = f.read()
        file_data_hex = b'\x7E\x41\x42\x43\x44\x45\x46\xE0\x55\x56\x57\x58\x59\x5A\xE1\x03\xF0\x0A\x07\x67\x45\x23\x01\xBB\xAA\x01\x00\xA2\x03\x22\xC8\x7E'
        file_data_bin = bitarray('01010101010101010101010101111110010000010100001001000011010001000100010101000110111000000101010101010110010101110101100001011001010110101110000100000011111010000000010100000011101100111010001010010001100000001101110111010101000000001000000001010001000000011001000101100100001111110')
        file_data = file_data_bin.tobytes()
        # file_data = b'\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x01\x01\x01\x01\x01\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x01\x00\x00\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x01\x01\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x01\x00\x01\x00\x01\x00\x00\x00\x01\x01\x00\x01\x01\x01\x00\x00\x00\x00\x00\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x00\x01\x01\x00\x00\x01\x00\x01\x00\x01\x01\x01\x00\x01\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x01\x00\x01\x00\x01\x01\x00\x01\x00\x01\x01\x01\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x01\x01\x01\x01\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x01\x00\x01\x01\x00\x00\x01\x01\x01\x00\x01\x00\x00\x00\x01\x00\x01\x00\x00\x01\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x01\x01\x01\x00\x01\x01\x01\x00\x01\x00\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x00\x00\x01\x01\x00\x00\x00\x00\x01\x00\x01\x01\x00\x00\x00\x01\x00\x00\x01\x01\x00\x00\x00\x01\x01\x00\x01\x01\x00\x00\x01\x00\x00\x00\x01\x01\x00\x00\x01\x00\x01\x00\x01\x01\x00\x00\x01\x01\x00\x00\x01\x01\x00\x00\x01\x01\x01\x00\x01\x01\x00\x01\x00\x00\x00\x00\x01\x01\x00\x01\x00\x00\x01\x00\x01\x01\x00\x01\x00\x01\x00\x00\x01\x01\x00\x01\x00\x01\x01\x00\x01\x01\x00\x01\x01\x00\x00\x00\x01\x01\x00\x01\x01\x00\x01\x00\x01\x01\x00\x01\x01\x01\x00\x00\x01\x01\x00\x01\x01\x01\x01\x01\x00\x00\x00\x01\x00\x00\x01\x01\x00\x01\x00\x00\x01\x01\x00\x01\x00\x01\x01\x01\x01\x01\x01\x00'
        # data_str = ''
        # barr = bitarray()
        # barr.frombytes(file_data_hex)
        # file_data = b''
        # for b in barr.to01():
        #     file_data += bytes([int(b)])
        file_data_length = len(file_data)


    ps_thread = ProcessThread(name = "ProcessThread") 
    tm_thread = TMThread(name = "TelemetryThread") 
    tm_thread.setDaemon(True)

    ps_thread.start()
    tm_thread.start()

    ps_thread.join()
    tm_thread.join()

