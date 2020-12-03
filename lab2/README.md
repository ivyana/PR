## Network Programming - Lab2

## Tasks:
1. Implement a protocol atop UDP, with error checking and retransmissions. 
Limit the number of retries for retransmission.

2. Make the connection secure, using either a CA to get the public key of the receiver and encrypt data with it, 
or using Diffie-Helman to get a shared connection key between client and server, ensure that the traffic is encrypted.

3. Regarding the application-level protocol, there are 3 options:
  - make an FTP-like protocol for data transfer, thus you will need to ensure data splitting and in-order delivery and reassembly at the destination. The protocol must support URIs, file creation and update (PUT), file fetching (GET) and metadata retrieval (OPTIONS)
  - make a protocol based on the workings (state machine) of an ATM
  - make a protocol based on the workings (state machine) of a stationary telephone 

### Implementation:

My project has a server-client architecture which runs on a protocol atop UDP with features of TCP. 

The TCP like attributes are the following:
- **checksums** (values used to verify the integrity of a file or a data transfer 
which are typically used to compare two sets of data to make sure they are the same)
- **sequence numbers** (they are used to coordinate which data has been transmitted 
and received and they will help to arrange for retransmission if data has been lost)
- **timer** (they are here to ensure that excessive delays are not encountered during communication)

Bonus: *Go-back-N protocol* implementation (this protocol uses a sliding window method for reliable and sequential delivery of 
data frames; it provides for sending multiple frames before receiving the acknowledgment for the first frame; this fact 
means that is a more efficient to use such method because during the time that would otherwise be spent waiting, more packets 
are being sent)

**Using all from above, I have focused on creating something like a FTP protocol for data transfer which ensures data 
splitting, in-order delivery and reassembly at the destination.**

### Implementation Details:

Here I will explain every module that I have in my project.
*If more info is needed, see the multiple comments in every particular module.*

So, I will start with the smallest ones: *1. globals.py* and *2. utils.py*

1. In *globals.py* module, I have IP address(localhost is the IP address my machine), port number(I used 5005 porn number), 
buffer_size(is set to 1024 -> packet size is 1024 with sequence number 1 byte, checksum 2 bytes, data 1021 bytes) 
which will be used later. Also, here I set the window size for the Go-Back-N protocol.

2. The module *utils.py* is used to store different useful functions like: calc_file_size (*Finds the file size with the 
help of seek function*), calc_loop_times (*Finds how many loops the program has to run to transfer the file*), 
update_seq_number (*Updates the sequence number*), calc_checksum (*Finds the Checksum for the data*), 
is_error_condition (*Finds if the bit_error has to happen or not*), corrupt_data (*Corrupts the data*), 
extract_data (*Extracts data (sequence number, checksum, data) from packet*), 
make_packet (*Makes packets (sequence number + checksum + data -> together forms a packet)*).

Next are *3. rdt_send.py* and *4. rdt_receive.py* which are Reliable Data Transfer functions:

3. Here, Packet is created with the sequence number, checksum, data + Buffer size of window size is created and 
data is added to the buffer. Also, here is the implementation of timers and sequence numbers for
every packet. For testing purposes, here I have used functions which drop packets or corrupt data intentionally(the
probability can be set in *client.py*).

4. Here is checked if the data was received successfully. The function from this module extracts the sequence number, 
checksum value, data from a packet. If packet is not corrupted and has expected sequence number, sends Acknowledgement 
with sequence number (*updates sequence number for next loop). If packet is corrupted or has unexpected sequence number,
sends Acknowledgement with previous Acknowledged sequence number and requests client to resend the data. (Here, we can
also introduce error or drop packets probability from *server.py*).

Last, but not the least, I have *5. client.py* and *6. server.py* (*In this 2 modules you can choose the probability of 
getting errors. This is done for testing purposes.*):

5. In client we work with time_buffer, image_buffer, opening the udp sockets and the file which will be transferred 
to the server. Also, here is calculated the size of image and how many loops we will need to send it. A loop runs until 
sequence number is equal to loop value. After that, is called the function rdt_send to send the packet. When the sending 
process is done, File and Socket are closed and we get the end time and the elapsed time for the client.

6. The server will bind the socket and will start to wait for clients. It will receive the size of file from client and 
will create a new file to store the received data. The server will call the function rdt_receive_packet to receive 
packets from client and will write the data to mentioned new file. As in client,  in the end, New File and Socket will be
closed and we will have the end time and the elapsed time for the server.

(*Note: For now, I didn't implement the security part.*)

### Instructions:
**Choose an image, change its name to *sent_image.jpg* and put it in the same folder as the project.**

**Run server:**
```
python server.py
```

**Run client:**
```
python client.py
```

**Voilà, the image has been sent from client to server:)**

### Output Examples:

**Server without errors:**
![alt text](https://github.com/ivyana/PR/blob/main/lab2/output/1.PNG)
![alt text](https://github.com/ivyana/PR/blob/main/lab2/output/2.PNG)

**Client without errors:**
![alt text](https://github.com/ivyana/PR/blob/main/lab2/output/3.PNG)
![alt text](https://github.com/ivyana/PR/blob/main/lab2/output/4.PNG)

**Here was introduced error and dropping packets probability:**
![alt text](https://github.com/ivyana/PR/blob/main/lab2/output/5.PNG)


