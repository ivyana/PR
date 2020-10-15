## Network Programming - Lab1 

### Implementation:

1. Pull a docker container (alexburlacu/pr-server) from the registry and run it (by forwarding the port 5000 to a port on local machine);
2. Access the root route of the server and find the way to /register;
3. Get the access token from /register;
4. Put the access token in an HTTP header of subsequent requests under the X-Access-Token key;
4. Extract data from data key and get next links from link key;
5. Use only one token(register) per program run;
6. Convert the fetched data to a common representation(json in my case);
10. Make a concurrent TCP server, serving the fetched content, that will respond to (mandatory) a 
column selector message, like `SelectColumn column_name`, and (optional) `SelectFromColumn column_name glob_pattern` (only SelectColumn for now);

### Instructions:
**Get docker container:**
```
docker pull alexburlacu/pr-server
docker run -p5000:5000 alexburlacu/pr-server
```

**Run server:**
```
python server.py
```

**Run client:**
```
python client.py
```
