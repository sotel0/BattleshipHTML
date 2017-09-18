#!/usr/bin/python3

import http.client  # module for python3
import sys          # reading input
# import requests

# function to write the unknown board to html
def writeOpponentBoard(Board):
    file = open("Opponent_Board.html", "w")
    x = 0
    boardStr = ""

    # for every character in the board
    for char in Board:
        file.write(char + "&nbsp;")
        x += 1
        if (x % 10 == 0):  # if we hit the end of a row, do a endline
            file.write("<br />")

    file.write("""<html><head></head><body><p>""" + boardStr + """</p></body></html>""")
    file.close()
    return


# get http server ip
serverIP = sys.argv[1]
port_num = sys.argv[2]
locationX = sys.argv[3]
locationY = sys.argv[4]

# create a connection
conn = http.client.HTTPConnection(serverIP, port_num)

urlString = "x="+ locationX + "&y=" + locationY

# headers = {"Content-type" : urlString, "Content2" : "777"}
headers = {"Content-type" : "text"}

# r = requests.get("", urlString)

# send request to server
# first input should be POST/'fire' command
# second input should be board location

conn.request("POST", "", urlString)

# get response from server
rsp = conn.getresponse()

# print server response and status

print("Response status:", end="")
print(rsp.status)

# updating opponent's board
# writeOpponentBoard(rsp.reason)


# print the returned data
data_received = rsp.read()
print("BODY: ", end="")
print(data_received)

# use data received to update opponent board


# conn.request("GET","/Own_Board.html")
# data = rsp.read()
# file = open(data, "w")

conn.close()

