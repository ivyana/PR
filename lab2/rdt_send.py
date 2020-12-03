from globals import *
import utils
import time
import socket

'''This function is the client's RDT(Reliable Data Transfer) function to send the file.'''


def rdt_send_packet(f, udp_sock, address, seq_number, data, e_prob=0, p_drop=0, window_size=0, base=0, loop=0,
                    image_buffer=None, time_buffer=None):
    if image_buffer is None:
        image_buffer = []
    if time_buffer is None:
        time_buffer = []
    if seq_number < (base + window_size):  # Check for empty slots in the windows
        while (seq_number < base + window_size) and (seq_number <= loop):  # Condition for GBN protocol (Sliding window)
            if seq_number > 0:  # Initially file size is sent through sequence number 0
                data = f.read(buffer_size - 4)
            packet = utils.make_packet(seq_number, utils.calc_checksum(data),
                                       data)  # Packet is created with the sequence number, checksum, data
            # Buffer size of window size is created and data is added to the buffer
            image_buffer[seq_number % window_size] = packet
            udp_sock.sendto(packet, address)  # Sends the data
            print("Packet Number_Sliding Window: ", seq_number)
            time_buffer[seq_number % window_size] = time.time()  # Time buffer stores the start time for each packet
            seq_number += 1  # Sequence number is updated by 1
        print("Start timer...")
    try:  # This is used for timer -> If timed-out, it comes out of try loop and goes to exception
        # UDP Socket timer is added here
        # In this case 30 milliseconds is set as timer
        # If timed-out before operation, it goes to the timer exception
        udp_sock.settimeout(0.03)
        ack_packet, address = udp_sock.recvfrom(buffer_size)  # Client receiving the acknowledgement packet
        # It is equivalent to sock.setblocking(0).
        # Timer is activated only for receive function which takes care of entire operation according to the FSM
        udp_sock.settimeout(None)

        # If Data_bit_error is true, it starts to drop packets intentionally
        # The received packets are not utilised/used. Also, ack packet is not dropped for the last window
        if (utils.is_error_condition(p_drop)) and (seq_number < loop - window_size):
            # As per the FSM, we need to time-out
            # Here we are using while loop
            # If current-time is less than the timer-time, it runs infinite loop with no operations
            # After timer-time, condition fails and loop comes out
            while time.time() < (time_buffer[base % window_size] + 0.03):
                pass
            print("############################ ACK PACKET DROPPED ################################\n")
            # Raise OSError
        else:
            # If data_bit_error is False, then it refers to No-packet dropping
            # It goes to else loop and utilises the received packet

            # Extracts the sequence number, checksum value, data from a packet
            packet_seq_number, sender_checksum, ack_data = utils.extract_data(ack_packet)

            # If data_bit_error is True, it starts to corrupt data intentionally
            # Also last window packets are not corrupted
            if (utils.is_error_condition(e_prob)) and (seq_number < loop - window_size):
                ack_data = utils.corrupt_data(ack_data)  # Function to corrupt data
                print("############################ ACK CORRUPTED ################################")

            ack_checksum = utils.calc_checksum(ack_data)  # Finds the checksum for received acknowledgement
            ack_data = ack_data.decode("UTF-8")  # Decodes from byte to integer for the comparison
            # Gets the integer value alone from the ACK
            # For example, if string 'ACK500' is the input then the output will be integer of 500
            ack_data_int = int(ack_data[3:len(ack_data)])
            print("ACK from Server: ", ack_data_int)

            '''Comparing Acknowledgement'''
            # If packet is not corrupted and has expected sequence number
            if (ack_data_int >= base) and (ack_checksum == sender_checksum):
                base = ack_data_int + 1  # Base value is the next value to the ack value
                print("ACK is OKAY: ", ack_data)
                print("Updated Base: ", base)
                print("Stop timer...\n")

            elif ack_checksum != sender_checksum:  # If packet is corrupted, it resends the packet
                print("ACK is NOT OKAY:{} \n".format(ack_data))  # Do Nothing

    except (socket.timeout, OSError):
        print("############################ SOCKET TIMED OUT ################################")
        print("Base: ", base)
        for i in range(base, seq_number):  # Resends the entire packet
            time_buffer[i % window_size] = time.time()  # Restarting the timer, updating start time for the packet
            udp_sock.sendto(image_buffer[i % window_size], address)  # Sending the data
            print("Sending the packet: ", i)
        print("\n")
    return seq_number, base  # Returns updated sequence number, base value
