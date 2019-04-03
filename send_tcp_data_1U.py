import struct
from utils.tcp_utils import TCPClient
import threading
from time import sleep
from queue import Queue

IP = 'localhost'
PORT = 5000

CC1020_ISR_STATE_INIT = 1
CC1020_ISR_STATE_TX_PREAMBLE = 5
CC1020_ISR_STATE_TX_FLAG = 6
CC1020_ISR_STATE_TX_DATA = 7
CC1020_ISR_STATE_TX_STUF = 8

packet_queue = Queue(maxsize=3)

class TransmitThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.taskState = CC1020_ISR_STATE_INIT
        self.ax_counter = 0
        self.frameIndex = 0
        self.tx_buffer = None
        self.bit_counter = 0
        self.byte = 0 

        self.client = TCPClient(IP, PORT)
        # Connect to TCP server
        connected = self.client.connect()
        if connected:
            print('Connection Successful')
        else:
            print('Failed to connect')

    def run(self):
        while(1):
            if not packet_queue.empty():
                self.tx_buffer = packet_queue.get()
                print(self.tx_buffer)

            self.transmit_task()

    def transmit_bit(self, bit):
        if bit:
            sent = self.client.send_data(b'\x01')
        else:
            sent = self.client.send_data(b'\x00')

        return sent

    def transmit_task(self):
       
        if self.taskState == CC1020_ISR_STATE_INIT:
            self.frameIndex = 0
            self.taskState = CC1020_ISR_STATE_TX_PREAMBLE
            self.byte = 0x55 #Preamble value

        elif self.taskState == CC1020_ISR_STATE_TX_PREAMBLE:
            if (self.byte & 0x80):
                self.transmit_bit(1)
            else:
                self.transmit_bit(0)
            self.bit_counter += 1
            if (self.bit_counter == 8):
                self.bit_counter = 0
                self.byte = 0x55 # Preamble value
                if self.tx_buffer is not None:
                    print("there is data")
                    self.byte = 0x7E # Flag
                    self.taskState = CC1020_ISR_STATE_TX_FLAG
                    return 0
            else:
                self.byte <<= 1

            return 0

        elif self.taskState == CC1020_ISR_STATE_TX_FLAG:
            if (self.byte & 0x80):
                self.transmit_bit(1)
            else:
                self.transmit_bit(0)
            self.bit_counter += 1
            if (self.bit_counter == 8):
                self.bit_counter = 0
                if (self.frameIndex):
                    self.taskState = CC1020_ISR_STATE_INIT
                    return self.frameIndex

                self.byte = self.tx_buffer[self.frameIndex] # Load first element
                self.taskState = CC1020_ISR_STATE_TX_DATA
                return 0
            else:
                self.byte <<= 1
            return 0

        elif self.taskState == CC1020_ISR_STATE_TX_DATA:
            if (self.byte & 0x80):
                self.ax_counter += 1
                self.transmit_bit(1)
            else:
                self.ax_counter = 0
                self.transmit_bit(0)

            self.bit_counter += 1
            if (self.ax_counter == 5):
                self.ax_counter = 0
                self.taskState = CC1020_ISR_STATE_TX_STUF
                return 0

            if (self.bit_counter == 8):
                self.bit_counter = 0
                if (self.frameIndex == len(self.tx_buffer)-1):
                    self.byte = 0x7E # Flag
                    self.tx_buffer = None
                    self.taskState = CC1020_ISR_STATE_TX_FLAG
                    return 0

                self.frameIndex += 1
                self.byte = self.tx_buffer[self.frameIndex] # Load next element

                return 0
            else:
                self.byte <<= 1
            
            return 0

        elif self.taskState == CC1020_ISR_STATE_TX_STUF:
            self.transmit_bit(0)
            if (self.bit_counter == 8):
                self.bit_counter = 0
                self.frameIndex += 1
                self.byte = self.tx_buffer[self.frameIndex] # Load next element
                if (self.frameIndex > len(self.tx_buffer)-1):
                    self.byte = 0x7E # Flag
                    self.taskState = CC1020_ISR_STATE_TX_FLAG
                    self.tx_buffer = None
                    return 0

            self.taskState = CC1020_ISR_STATE_TX_DATA
            return 0

        else:
            self.taskState = CC1020_ISR_STATE_INIT
            return 0


class TCThread(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        while(1):
            print("adding data")
            sleep(1)
            # Payload with no stuffing
            data = b'\x41\x42\x43\x44\x45\x46\xE0\x55\x56\x57\x58\x59\x5A\xE1\x02\xF0\x0A\x07\x67\x45\x23\x01\xBB\xAA\x01\x00\xA2\x03\x59\xA9'

            # Payload with stuffing
            # data = b'\x41\x42\x43\x44\x45\x46\xE0\x55\x56\x57\x58\x59\x5A\xE1\x02\xF0\x0A\x07\x67\x45\x23\x01\xBB\xAA\x01\x00\xA2\x03\x98\xFB'

            packet_queue.put(data)


if __name__ == "__main__":
    try:
        tx_thread = TransmitThread(name = "TransmitThread") 
        tx_thread.start()
        tc_thread = TCThread(name = "TelecommandThread") 
        tc_thread.start()

    except:
        print("error")
        # print('Received Packets found:', tx_thread.received_packets)
        # print('Valid Packets found:', tx_thread.valid_packets