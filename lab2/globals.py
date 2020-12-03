import time

# Find the start time of the program, elapsed time can be found by end time - start time
start = time.time()

'''Importing IP address, port number, buffer_size'''
UDP_IP = "localhost"  # Localhost is the IP address of machine
UDP_PORT = 5005  # Port Number is assigned to 5005
# buffer_size is set to 1024 -> packet size is 1024 with sequence number 1 byte, checksum 2 bytes, data 1021 bytes
buffer_size = 1024
addr = (UDP_IP, UDP_PORT)

'''For the GBN(Go back N Protocol) sliding window, setting the window_size value'''
# Set the window size for the Go-Back-N protocol.
# This window_size is only for the client program for the sliding window.
# Server side window_size is always 1.
# Client window_size also included in Server program ONLY to avoid intentional packet corrupt/drop for the last window.
window_size = 5
