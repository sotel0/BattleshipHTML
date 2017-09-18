#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import re
import socket # just used to get local ip


# C - 5, B - 4, R - 3, S - 3, D - 2
# used to keep track of which ships have been sunk
shipList = [5, 4, 3, 3, 2]


# Create custom HTTPRequestHandler class
class HTTPHandler(BaseHTTPRequestHandler):

    # define update request
    def do_GET(self):
        try:

            print("####@#@#@#@")
            print (self.rfile.read(7))

            fileB = open("own_board.html")
            self.response(200)
            self.send_header('Content-type', 'file')
            self.end_headers()
            self.wfile.write(fileB)
            return
        except IOError:
            self.send_error(404, 'file not found')

    # define post/fire request
    def do_POST(self):
        infile = open('Board.txt', 'r')
        ownBoard = readInBoard(infile)
        infile2 = open('enemyBoard.txt', 'r')
        guessBoard = readInBoard(infile2)

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

                urlResponse = ""

                response, sunk, guessBoard = makeGuess(ownBoard, guessBoard, row, col)
                if response == 1 or response == 0:
                    if response == 1:
                        urlResponse = "hit=1"
                    else:
                        urlResponse = "hit=0"

                    if sunk == 0:
                        pass
                    else:
                        letter = getLetter(sunk)
                        urlResponse = urlResponse + "&sink=" + letter
                    response = 200

                # send file content to client

            # write the response back
            print(response)
            self.send_response(response)

            self.send_header('Content-type', 'text')
            self.end_headers()

            self.wfile.write(bytes(urlResponse, "utf-8"))

            return

        except IOError:
            self.send_error(404, 'file not found')


def checkFormat(spot):
    if len(spot) != 10:
        return False
    if spot[2] != "x" or spot[3] != "=" or spot[5] != "&" or spot[6] != "y" or spot[7] != "=":
        return False
    if spot[4] == "1" or spot[4] == "2" or spot[4] == "3" or spot[4] == "4" or spot[4] == "5" or spot[4] == "6" or spot[4] == "7" or spot[4] == "8" or spot[4] == "9":
        pass
    if spot[8] == "1" or spot[8] == "2" or spot[8] == "3" or spot[8] == "4" or spot[8] == "5" or spot[8] == "6" or spot[8] == "7" or spot[8] == "8" or spot[8] == "9":
        pass
    return True



def readInBoard(infile):
    boardStr = ''
    # Loop through each line of the file
    for line in infile:
        line = re.sub("\n", '', line)  # delete endlines
        boardStr += line
    return boardStr


def main():

    # create empty board for guesses to be placed

    infile = open('enemyBoard.txt', 'w')

    for i in range(10):
        if i != 9:
            infile.write("__________\n")
        else:
            infile.write("__________")
    infile.close()

    print('starting server...')

    # gets port from arguments
    port_number = int(sys.argv[1])

    # gets own IP number, can change to desired IP
    IP = socket.gethostbyname(socket.gethostname())
    print("Server IP: " + IP)
    server_address = (IP, port_number)

    # establish httpd server
    httpd = HTTPServer(server_address, HTTPHandler)
    print('http server is running...')
    httpd.serve_forever()


def makeGuess(ownBoard, guessBoard, row, col):

    # represent the whole board as one list of integers
    guess = row * 10 + col

    # check if the guess missed or you chose a spot you already hit
    if row > 9 or col > 9:
        return 404, 0, guessBoard

    elif guessBoard[guess] == 'X' or guessBoard[guess] == 'O':
        print("You already guessed that spot")
        return 410, 0, guessBoard

    elif ownBoard[guess] == '_':
        print("That one missed")

        # switch out the that spot for a 'missed hit' marker
        guessBoard = guessBoard[:guess] + 'X' + guessBoard[guess + 1:]
        ownBoard = ownBoard[:guess] + 'X' + ownBoard[guess + 1:]

        writeMyBoard(ownBoard)
        writeOpponentBoard(guessBoard)

        return 0, 0, guessBoard
    else:  # that probably was a hit
        print("You hit a: " + ownBoard[guess])
        letter = ownBoard[guess]

        # C, B, R, S, D
        global shipList

        index = getIndex(letter)
        shipList[index] = shipList[index] - 1
        if shipList[index] <= 0:
            return 1, letter, guessBoard
        # switch out the that spot for a 'hit a ship' marker
        guessBoard = guessBoard[:guess] + 'O' + guessBoard[guess + 1:]
        ownBoard = ownBoard[:guess] + 'O' + ownBoard[guess + 1:]

        writeMyBoard(ownBoard)
        writeOpponentBoard(guessBoard)

        return 1, 0, guessBoard

def writeOpponentBoard(Board):
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


# write the
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