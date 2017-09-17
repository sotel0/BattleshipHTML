#!/usr/bin/python3

import http.client  # module for python3
import sys          # reading input

# get http server ip
serverIP = sys.argv[1]
port_num = sys.argv[2]

# create a connection
conn = http.client.HTTPConnection(serverIP, port_num)

while 1:
    # prompt client for input
    cmd = input('type command: ')
    cmd = cmd.split()

    # quit connection if exit
    if cmd[0] == 'exit':
        break

    # send request to server
    # first input should be POST/'fire' command
    # second input should be board location
    conn.request(cmd[0], cmd[1])

    # get response from server
    rsp = conn.getresponse()

    # print server response and data
    print(rsp.status, rsp.reason)
    data_received = rsp.read()
    print(data_received)

conn.close()