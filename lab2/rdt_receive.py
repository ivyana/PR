import utils


'''This function is the the Server's RDT(Reliable Data Transfer) function to receive the file.'''


def rdt_receive_packet(sock, buffer_size, rx_seq_number, e_prob=0, p_drop=0, loop=0, window_size=0):
    receive_successful = 0  # Receive_successful is set to '0' initially

    while not receive_successful:  # Loop goes on until condition becomes 'false'

        data, address = sock.recvfrom(buffer_size)  # Packet is received from client

        # If Data_bit_error is True, it starts to Drop packets intentionally by coming out of while-loop
        # The received packets are not utilised/used. Also, packet is not dropped for the last window
        if (utils.is_error_condition(p_drop)) and (rx_seq_number < loop - window_size):
            print("############################ DATA PACKET DROPPED ################################\n")
            receive_successful = 0  # Comes out of current loop and starts again since condition will be while(1).

        else:
            # If data_bit_error is False,then it refers to No-packet dropping
            # It goes to else loop and utilises the received packet

            # Extracts the sequence number, checksum value, data from a packet
            seq_num, checksum, img_packet = utils.extract_data(data)

            # If data_bit_error is True, it starts to corrupt packet intentionally
            # Also, ack packet is not corrupted for the last window
            if (utils.is_error_condition(e_prob)) and (rx_seq_number < loop - window_size):
                img_packet = utils.corrupt_data(img_packet)  # Function to corrupt data
                print("############################ DATA CORRUPTED ################################\n")

            rx_checksum = utils.calc_checksum(img_packet)  # Receiver Checksum in integer

            # If packet is not corrupted and has expected sequence number,
            # sends Acknowledgement with sequence number *updates sequence number for next loop
            if ((rx_checksum == checksum) and (
                    seq_num == rx_seq_number)):
                ack = rx_seq_number  # Sends sequence number as ACK
                # Converting (ack) from int to string and then encoding to bytes
                ack = b'ACK' + str(ack).encode("UTF-8")
                # Server sends ack with expected seq_number (Next Sequence Number), checksum, ack
                sender_ack = utils.make_packet(seq_num + 1, utils.calc_checksum(ack), ack)
                print("Sequence Number: {0}, Receiver Sequence Number: {1}, Checksum from Client: {2}, "
                      "Checksum for Received File: {3}\n".format(seq_num, rx_seq_number, checksum, rx_checksum))
                rx_seq_number = 1 + seq_num  # Update sequence number to the next expected seq_number
                receive_successful = 1  # Comes out of while loop

            # If packet is corrupted or has unexpected sequence number,
            # sends Acknowledgement with previous Acknowledged sequence number
            # Requests client to resend the data
            elif (rx_checksum != checksum) or (seq_num != rx_seq_number):
                ack = rx_seq_number - 1  # last acknowledged sequence number
                # Converting (ack) from int to string and then encoding to bytes
                ack = b'ACK' + str(ack).encode("UTF-8")
                # Server sends ack with Seq_num, checksum, ack
                sender_ack = utils.make_packet(rx_seq_number, utils.calc_checksum(ack), ack)
                # print("Sequence Number: {0},Receiver_sequence: {1}\n".format(seq_num,Rx_seq_num))
                receive_successful = 0  # Loop continues until satisfies condition
            sock.sendto(sender_ack, address)  # sending the Acknowledgement packet to the client

    return img_packet, address, rx_seq_number  # Returns data,address,updated sequence number
