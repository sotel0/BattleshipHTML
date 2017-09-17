#!/usr/bin/python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
import os


# Create custom HTTPRequestHandler class
class HTTPHandler(BaseHTTPRequestHandler):

    # define POST command
    def do_POST(self):

        # rootdir = 'C:\\Users\Ar\Desktop\Battleship'  # file location
        # print(os.path.dirname(os.path.abspath(__file__)))

        try:
            #     f = open(self.path)  # open requested file
            #     # os.path.realpath(__file__)

            # access POST data
            ####fails
            # content_len = int(self.headers.getheader('content-length'))
            # post_body = self.rfile.read(content_len)
            # print(post_body)

            # OK code response
            self.send_response(200)

            # send headers
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            #     # send file content to client
            #     self.wfile.write(f.read())
            #     f.close()
            return

        except IOError:
            self.send_error(404, 'file not found')


def main():

    print('starting server...')

    # set ip and port for server
    port_number = int(sys.argv[1])

    # server_address = ('128.111.52.24', port_number)
    server_address = ('153.90.68.36', port_number)
    # server_address = ('127.0.0.1', port_number)

    # establish httpd server
    httpd = HTTPServer(server_address, HTTPHandler)
    print('http server is running...')
    httpd.serve_forever()


if __name__ == '__main__':
    main()