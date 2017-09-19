#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys    # using arguments
import re     # string management
import socket # just used to get local ip
import fileinput #to get the board file

# C - 5, B - 4, R - 3, S - 3, D - 2
# used to keep track of which ships have been sunk
shipList = [5, 4, 3, 3, 2]
firstTime = True
boardfile = ""

# Create custom HTTPRequestHandler class
class HTTPHandler(BaseHTTPRequestHandler):

    # define request to return html file
    def do_GET(self):
        try:

            if self.path == '/opponent_board.html':
                with open('opponent_board.html') as fh:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(fh.read().encode())

            if self.path == '/own_board.html':
                with open('own_board.html') as fh:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(fh.read().encode())
            return
        except IOError:
            self.send_error(404, 'file not found')

    # define post/fire request
    def do_POST(self):
        global firstTime

        # create copy of board.txt if first load up
        if firstTime:
            firstTime = False

            # copy board.txt into tempBoard.txt
            with open(boardfile) as f:
                with open("tempBoard.txt", "w") as f1:
                    for line in f:
                        f1.write(line)

        # use tempBoard when editing directly
        infile = open("tempBoard.txt", "r")

        ownBoard = readInBoard(infile)

        try:
            # declare response as global
            global response
            global urlResponse

            # getting the location of attack
            x = str(self.rfile.read(7))

            # Check if the format of url is correct
            correct_format = checkFormat(x)
            if not correct_format:
                response = 400
            else:

                # update the location variables
                col = int(x[4])
                row = int(x[8])

                # create response to be sent
                urlResponse = ""

                response, sunk = makeGuess(ownBoard, row, col)
                if response == 1 or response == 0:
                    if response == 1:
                        urlResponse = "hit=1"
                    else:
                        urlResponse = "hit=0"

                    if sunk == 0:
                        pass
                    else:
                        urlResponse = urlResponse + "&sink=" + sunk
                    response = 200

                # send file content to client

            # write the response back
            self.send_response(response)

            self.send_header('Content-type', 'text')
            self.end_headers()

            self.wfile.write(bytes(urlResponse, "utf-8"))

            return

        except IOError:
            self.send_error(404, 'file not found')

def main():
    global boardfile
    boardfile = sys.argv[2]

    print('starting server...')

    # gets port from arguments
    port_number = int(sys.argv[1])
    print(("Server Port: " + str(port_number)))

    # gets own IP number, can change to desired IP

    # uncomment/comment local host to use / not use
    IP = socket.gethostbyname(socket.gethostname())
    #IP = "127.0.0.1"

    print("Server IP: " + IP)
    server_address = (IP, port_number)


    # establish httpd server
    httpd = HTTPServer(server_address, HTTPHandler)
    print('http server is running...')
    httpd.serve_forever()


def checkFormat(spot):
    if len(spot) != 10:
        return False
    if spot[2] != "x" or spot[3] != "=" or spot[5] != "&" or spot[6] != "y" or spot[7] != "=":
        return False
    if spot[4] == "1" or spot[4] == "2" or spot[4] == "3" or spot[4] == "4" or spot[4] == "5" or spot[4] == "6" or spot[4] == "7" or spot[4] == "8" or spot[4] == "9":
        pass
    else:
        return False
    if spot[8] == "1" or spot[8] == "2" or spot[8] == "3" or spot[8] == "4" or spot[8] == "5" or spot[8] == "6" or spot[8] == "7" or spot[8] == "8" or spot[8] == "9":
        pass
    else:
        return False
    return True


# turn the file into a string
def readInBoard(infile):
    boardStr = ''
    # Loop through each line of the file
    for line in infile:
        line = re.sub("\n", '', line)  # delete endlines
        boardStr += line
    return boardStr


# update the tempBoard
def overwriteFile(board):
    file = open("tempBoard.txt", "w")
    for i in range(1,101):

        if i != 0 and i % 10 == 0:
            file.write((board[i-1]))
            file.write("\n")
        else:
            file.write((board[i-1]))
    file.close()
    return


def makeGuess(ownBoard, row, col):

    # represent the whole board as one list of integers
    guess = row * 10 + col

    # check if it is out of bounds
    if row > 9 or col > 9:
        return 404, 0

    # check if the guess was a spot already hit
    elif ownBoard[guess] == 'X' or ownBoard[guess] == 'O':
        print("Already guessed that spot")
        return 410, 0

    # check if the guess missed
    elif ownBoard[guess] == '_':
        print("That one missed")

        # switch out that spot for a 'missed hit' marker
        ownBoard = ownBoard[:guess] + 'X' + ownBoard[guess + 1:]

        overwriteFile(ownBoard)
        writeMyBoard(ownBoard)

        return 0, 0
    else:  # that probably was a hit
        print("You hit a: " + ownBoard[guess])
        letter = ownBoard[guess]

        # C, B, R, S, D
        global shipList

        # switch out the that spot for a 'hit a ship' marker
        ownBoard = ownBoard[:guess] + 'O' + ownBoard[guess + 1:]

        overwriteFile(ownBoard)
        writeMyBoard(ownBoard)

        # return if it sunk or not
        index = getIndex(letter)
        shipList[index] = shipList[index] - 1
        if shipList[index] <= 0:
            return 1, letter

        return 1, 0


# function to write the enemy board to html
def writeMyBoard(Board):

    file = open("own_board.html", "w")
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


# convert from letter to number
def getIndex(letter):
    return {
        'C': 0,
        'B': 1,
        'R': 2,
        'S': 3,
        'D': 4
    }[letter]


# convert from number to letter
def getLetter(index):
    return {
        0: 'C',
        1: 'B',
        2: 'R',
        3: 'S',
        4: 'D'
    }[index]


if __name__ == '__main__':
    main()