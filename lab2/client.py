from globals import *  # Common variables
import utils  # Functions like checksum, file size, bit error, etc.
import rdt_send  # Reliable Data Transfer Send function
import socket
import struct

'''To corrupt data packet, Set value from 0 - 99 in e_prob'''
e_prob = 0  # e_prob is the error probability and can be set from 0-99
p_drop = 0  # p_drop is the packet dropping probability and can be set from 0-99

time_buffer = [None] * window_size  # Time_Buffer stores the start time for the packets
print("Window size: ", window_size)  # Prints the window size
image_buffer = [None] * window_size  # Stores the data in the buffer
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Socket with IPV4, UDP
f = open('sent_image.jpg', 'rb')  # Opening the file which will be transferred to the server

file_size = utils.calc_file_size(f)  # File size is calculated

loop = utils.calc_loop_times(file_size, buffer_size)  # Finding the loop value
loop_bytes = struct.pack("!I", loop)  # Change loop from integer to byte inorder to send data from client to server
print("File has been Extracted \nFile size: {0} \nNo. of Loops to send the entire file: {1}".format(file_size, loop))
seq_number = 0  # Sequence Number is set to 0 initially
base = 0  # Here base is set to 0
print('Client file transfer starts...')

while base <= loop:  # Loop runs until sequence number is equal to loop value. Sequence number starts from 1.
    # calls the function rdt_send to send the packet
    seq_number, base = rdt_send.rdt_send_packet(f, sock, addr, seq_number, loop_bytes, e_prob, p_drop,
                                                    window_size, base, loop, image_buffer, time_buffer)

f.close()  # File closed
sock.close()  # Socket Closed

end = time.time()  # Gets the End time
elapsed_time = end - start  # Gets the elapsed time
print("Client: File Sent\nFile size sent to server: {0}\nTime taken in Seconds:{1}s\n".format(file_size, elapsed_time))
