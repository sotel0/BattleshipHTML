#!/usr/bin/python3

import http.client  # module for python3
import sys          # reading input
import os           # file reading
import re           # string management


# function to write the enemy board to html
def writeOpponentBoard(Board):

    # copy new over enemyBoard
    file = open("opponent_board.html", "w")
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


# update the board
def overwriteFileC(board):
    file = open("enemyBoard.txt", "w")

    for i in range(1,101):

        if i != 0 and i % 10 == 0:
            file.write((board[i-1]))
            file.write("\n")
        else:
            file.write((board[i-1]))
    file.close()
    return


# turn a file into one string
def readInBoard(infile):
    boardStr = ''
    # Loop through each line of the file
    for line in infile:
        line = re.sub("\n", '', line)  # delete endlines
        boardStr += line
    return boardStr


def main():

    # create empty board for guesses to be placed if does not exists
    if not os.path.exists('enemyBoard.txt'):
        infile = open('enemyBoard.txt', 'w')

        for i in range(10):
                infile.write("__________\n")
        infile.close()

    # get http server ip
    serverIP = sys.argv[1]
    port_num = sys.argv[2]
    locationX = sys.argv[3]
    locationY = sys.argv[4]

    # create a connection
    conn = http.client.HTTPConnection(serverIP, port_num)

    # create the location to be sent
    urlString = "x=" + locationX + "&y=" + locationY

    # send request to server
    # first input should be POST/'fire' command
    # second input should be board location

    conn.request("POST", "", urlString)

    # get response from server
    rsp = conn.getresponse()
    data_received = rsp.read()

    # print server response and status
    print("Response status:", end="")
    print(rsp.status)

    # print the returned data
    print("DATA: ", end="")
    s = str(data_received, 'utf-8')
    print(s)
    # --------

    # updating opponent's board
    infile = open("enemyBoard.txt", "r")
    guessBoard = readInBoard(infile)

    guess = int(locationY) * 10 + int(locationX)

    status = rsp.status
    if status == 404:
        print("missed")
    elif status == 410:
        print("already shot here")
    elif status == 200:

        s = str(data_received, 'utf-8')

        if s[4] == "0":
            guessBoard = guessBoard[:guess] + 'X' + guessBoard[guess + 1:]

        elif s[4] == "1":
            guessBoard = guessBoard[:guess] + 'O' + guessBoard[guess + 1:]

        overwriteFileC(guessBoard)
        writeOpponentBoard(guessBoard)


    # conn.request("GET","/Own_Board.html")
    # data = rsp.read()
    # file = open(data, "w")

    conn.close()


if __name__ == '__main__':
    main()