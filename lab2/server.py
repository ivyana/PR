from globals import *  # Common variables
import rdt_receive  # Reliable Data Transfer Receive function
import utils  # Functions like checksum, filesize, bit error, etc.
import socket
import struct

'''To corrupt ack packet, set value from 0 - 99 in e_prob'''
e_prob = 0  # e_prob is the error probability and can be set from 0-99
p_drop = 0  # p_drop is the packet dropping probability and can be set from 0-99

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket with IPV4, UDP
sock.bind(addr)  # Binding the socket
print("Server started...\nWaiting for clients...")

p = open('received_image.jpg', 'wb')  # Opening a new file to copy the transferred image

receiver_sequence = 0  # Server side sequence number is initialised to zero
# Receiving the file size from client
loopTimes, address, receiver_sequence = rdt_receive.rdt_receive_packet(sock, buffer_size, receiver_sequence)
loop = struct.unpack("!I", loopTimes)[0]  # Changing loop from byte to integer
print("Number of loops to send the entire file: ", loop)
print("Writing/Receiving process starting soon...\n")  # Receiving file from Client

while receiver_sequence <= loop:
    # Calls the function rdt_receive_packet to receive the packet
    image_packet, address, receiver_sequence = rdt_receive.rdt_receive_packet(sock, buffer_size, receiver_sequence,
                                                                               e_prob, p_drop, loop, window_size)
    p.write(image_packet)  # Writes/Stores the received data to a file

# File Received from Client at the end of Loop
Received_File_Size = utils.calc_file_size(p)  # Calculating Received Image file size

p.close()  # Closing the file
sock.close()  # Closing the socket

end = time.time()  # Finding the end-time
Elapsed_time = end - start  # Elapsed time
print("Server: File Received\nReceived File size: {0}\nTime taken in Seconds: {1}s".format(Received_File_Size,
                                                                                           Elapsed_time))
