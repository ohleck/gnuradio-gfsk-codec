from bitarray import bitarray
import struct

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

    bin_arr = '100000001010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101010101100100110011001100110011001100110011001100110011001100110011001100110011001110010110101010000110011111100111011111110'
    # encoded = encode_nrzi(bin_arr)
    output = decode_nrzi(bin_arr)
    # print('Input:', bin_arr)
    # print('Encoded:', encoded)
    print('Output:', output)

    # bin_arr = '111110111110101'
    # bin_arr = '111111111110111110101'

    # stuffed = add_stuffing(bin_arr)

    # output = remove_stuffing(stuffed)

    # print(bin_arr)
    # print(stuffed)
    # print(output)