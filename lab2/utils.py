import math
import random
import struct


'''Finds the file size with the help of seek function'''


def calc_file_size(file):
    file.seek(0, 2)  # Moves the file pointer to the EOF
    file_size = file.tell()  # Gets file size
    file.seek(0, 0)  # Moves the file pointer the the beginning of the file
    return file_size  # Returns the file size in integer


'''Finds how many loops the program has to run to transfer the file'''


def calc_loop_times(file_size, buffer_size):
    # File size is divided by buffer_size - 3 to find the loop_times, because 3 bytes will be the headers for the packet
    loop_times = (file_size / (buffer_size - 3))
    loop = math.ceil(loop_times)  # Changing loop_times to next integer
    return loop  # Returns the loop value in integer


'''Updates the sequence number'''


def update_seq_number(seq_number):
    return 1 - seq_number  # Returns 1-seq_number in integer


'''Finds the Checksum for the data'''


def calc_checksum(data):
    checksum_addition = 0  # Initial checksum value is zero
    for i in range(0, len(data), 2):  # Loop starts from 0 to len(data)-1, iterated +2 times.
        first_2bits = data[i: (i + 2)]  # taking 16 bits (2 bytes) value from 1024 bytes
        if len(first_2bits) == 1:
            two_byte_integer = struct.unpack("!B", first_2bits)[
                0]  # If len(data)=1 it has to be unpacked with standard size 1
        elif len(first_2bits) == 2:
            two_byte_integer = struct.unpack("!H", first_2bits)[
                0]  # If len(data)=2 it has to be unpacked with standard size 2
        checksum_addition = checksum_addition + two_byte_integer  # Checksum addition
        while (checksum_addition >> 16) == 1:  # Loop goes on until condition becomes 'false'
            checksum_addition = (checksum_addition & 0xffff) + (checksum_addition >> 16)  # Wrap up function
    return checksum_addition  # Returns checksum for the data in integer


'''Finds if the bit_error has to happen or not'''


def is_error_condition(e_prob=0):
    data_bit_error = False  # data_bit_error has been initialised as 'False'
    random_number = random.random()  # This generates a random probability value (0.00 to 1.00)
    # Convert percentage(e_prob) to probability [(0 to 100) into (0.00 to 1.00)] in order to compare with random_number
    if random_number < (e_prob / 100):
        data_bit_error = True  # If condition is 'True' it corrupts data
    return data_bit_error  # Returns data_bit_error as 'True' or 'False'


'''Corrupts the data'''


def corrupt_data(data):
    # Replacing the first two bytes of data with alphabet character 'X' in order to corrupt, returns in byte
    return b'XX' + data[2:]


'''Extracts data (sequence number, checksum, data) from packet'''


def extract_data(packet):  # Extracts the packet
    # Find the length of the data, (length of the sequence number (2byte) and checksum(2bytes) are fixed)
    data_len = len(packet) - struct.calcsize('HH')
    # This is the packet format. example if data length is 1020 bytes then it should be "!HH1020s"
    packet_format = "!HH" + str(data_len) + "s"
    return struct.unpack(packet_format, packet)  # Returns the unpacked values of packet.


'''Makes packets (sequence number + checksum + data -> together forms a packet)'''


def make_packet(seq_numbers, checksums, data):
    # This is the packet format. example if data length is 1020 bytes then it should be "!HH1021s"
    packet_format = "!HH" + str(len(data)) + "s"
    # Packs sequence number, checksum, data and forms a packet
    packet = struct.pack(packet_format, seq_numbers, checksums, data)
    return packet  # Returns packet in bytes
