from bitarray import bitarray
import struct


def compute_crc(bin_string):
    """Compute the CRC-CCITT checksum.

    Keyword arguments:
    bin_string -- Complete transfer frame [binary string]

    Outputs:
    checksum -- Computed checksum for the given bitstring [bytes]

    TODO: In line documenting

    """
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
    The CRC bytes are assumed to be in the last 16 bit positions of bin_arr.

    Keyword arguments:
    bin_arr -- Binary array [binary string]

    Outputs:
    boolean -- True if CRC valid, False otherwise

    '''
    payload_data_bin = bitarray(bin_arr[:-16])  # remove CRC
    if (len(payload_data_bin) % 8) != 0:
        return False
    crc_bin = bitarray(bin_arr[-16:])

    crc_calc = compute_crc(payload_data_bin.to01())

    return (int(crc_bin.to01(), 2) == int.from_bytes(crc_calc, byteorder='big'))


def assemble_hdlc_packet(preambule, flag, data):
    '''
    Assemble a HDLC packet compatible with AX5043 radio. The packet is formed by:
    Preamble (n bytes) + FLAG (1 byte 0x7E) + LENGTH (1 byte) + DATA (n bytes) + CRC (2 bytes) + FLAG (1 byte)
    
    LENGTH = Takes into account Length + Data bytes
    CRC = Computed for Length and Data bytes (crc-16-genibus)

    Additional info:
    - The LENGTH DATA and CRC bytes are stuffed
    - The Preamble is uncoded and unstuffed
    - The remaining bytes are coded as NRZI

    Keyword arguments:
    preambule -- Preamble bytes [bytes]
    flag -- Flag Bytes bytes [bytes]
    data -- Data bytes [bytes]

    Outputs:
    packet -- Encoded and sutffed HDLC packet [binary string]

    '''
    # Compute payload length
    payload_length = bitarray(bin(1 + len(data))[2:].zfill(8))
    payload = payload_length.tobytes() + data

    # Transform payload to bits
    payload_bin = bitarray()
    payload_bin.frombytes(payload)

    # Compute Checksum
    crc = compute_crc(payload_bin.to01())

    # Transform checksum to bits
    crc_bin = bitarray()
    crc_bin.frombytes(crc)

    # Create inner hdlc packet: payload + CRC
    inner_hdlc_packet = payload_bin + crc_bin

    # Add stuffing to inner packet
    bin_inner_hdlc_packet_stuffed = add_stuffing(inner_hdlc_packet)

    # Transform flag to bits
    flag_bin = bitarray()
    flag_bin.frombytes(flag)

    # Create HDLC packet
    bin_hdlc_packet_stuffed = flag_bin.to01() + bin_inner_hdlc_packet_stuffed + header_bin.to01()

    # Encode packet as NRZI
    hdlc_packet_encoded = encode_nrzi(bin_hdlc_packet_stuffed)

    hdlc_packet_encoded_barr = bitarray(hdlc_packet_encoded)
    hdlc_packet_encoded_bytes = hdlc_packet_encoded_barr.tobytes()

    # Add preambule
    packet = preambule + hdlc_packet_encoded_bytes

    return packet


def encode_diff(bin_arr):
    '''
    Encode a bitstream as differential.

    Ref: http://www.ece.iit.edu/~biitcomm/research/references/Other/Tutorials%20in%20Communications%20Engineering/TUTORIAL%202%20-%20Differential%20Encoding.pdf

    Keyword arguments:
    bin_arr -- Binary array [binary string]

    Outputs:
    Encoded binary array [binary string]
    '''
    ref_bit = bitarray('1') # Using 1 as ref bit
    uncoded_bin_arr = bitarray(bin_arr)
    encoded_bin_arr = bitarray(ref_bit)
    for i in range(0, len(uncoded_bin_arr)):
        encoded_bin_arr.append(encoded_bin_arr[i] != uncoded_bin_arr[i])

    return encoded_bin_arr.to01()


def decode_diff(bin_arr):
    '''
    Decode a bitstream as differential.

    Ref: http://www.ece.iit.edu/~biitcomm/research/references/Other/Tutorials%20in%20Communications%20Engineering/TUTORIAL%202%20-%20Differential%20Encoding.pdf

    Keyword arguments:
    bin_arr -- Encoded Binary array [binary string]

    Outputs:
    Decoded binary array [binary string]
    '''
    uncoded_bin_arr = bitarray(bin_arr)
    decoded_bin_arr = bitarray('')
    for i in range(1, len(uncoded_bin_arr)):
        decoded_bin_arr.append(uncoded_bin_arr[i-1] != uncoded_bin_arr[i])

    return decoded_bin_arr.to01()


def encode_nrzi(bin_arr):
    '''
    Encode a bitstream according to NRZI scheme.

    Keyword arguments:
    bin_arr -- Binary array [binary string]

    Outputs:
    Encoded binary array [binary string]
    '''
    bits = bitarray(bin_arr)
    bits.invert()
    encoded = encode_diff(bits)

    return encoded


def decode_nrzi(bin_arr):
    '''
    Decode a bitstream according to NRZI scheme.

    Keyword arguments:
    bin_arr -- Encoded Binary array [binary string]

    Outputs:
    Decoded binary array [binary string]
    '''
    decoded = decode_diff(bin_arr)
    bits = bitarray(decoded)
    bits.invert()

    return bits.to01()


def add_stuffing(bin_arr):
    '''
    Add stuffing bits to 5x'1's sequences. The output should contain only '1' sequences 
    of length < 6

    Keyword arguments:
    bin_arr -- Binary array [binary string]

    Outputs:
    Stuffed binary array [binary string]
    '''
    barr = bitarray(bin_arr)
    i = 0
    # Traversing bin_array searching for five 1's in a row
    while i < (len(barr)-5):
        if barr[i] & barr[i+1] & barr[i+2] & barr[i+3] & barr[i+4]:
            barr.insert(i+5, False)
            i += 5

        i += 1

    return barr.to01()


def remove_stuffing(bin_arr):
    '''
    Remove stuffing bits after 5x'1's sequences.

    Keyword arguments:
    bin_arr -- Stuffed Binary array [binary string]

    Outputs:
    Unstuffed binary array [binary string]
    '''
    barr = bitarray(bin_arr)
    index = barr.search(bitarray('11111'))
    removed = 0
    for i in index:
        if i >= (len(barr)-5):
            continue
        barr.pop(i+5-removed)
        removed += 1

    return barr.to01()


if __name__ == "__main__":

    # data = bytes(range(8))
    # crc = compute_crc(data)
    # data_crc = data + crc
    # data_crc_bin = bitarray()
    # data_crc_bin.frombytes(data_crc)
    # valid_crc = check_crc(data_crc_bin.to01())
    # assert()


    bin_arr = '0010111101000010'
    encoded = encode_nrzi(bin_arr)
    output = decode_nrzi(encoded)
    print('Input:', bin_arr)
    print('Encoded:', encoded)
    print('Output:', output)

    # bin_arr = '111110111110101'
    # bin_arr = '111111111110111110101'

    # stuffed = add_stuffing(bin_arr)

    # output = remove_stuffing(stuffed)

    # print(bin_arr)
    # print(stuffed)
    # print(output)
