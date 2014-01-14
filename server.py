import SocketServer, os, errno
# coding: utf-8

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        toks = self.data.split()

        reply = ""

        # getting the full path to the file requested
        cwd = os.getcwd()
        wwwDir = os.path.join(cwd, "www")
        filename = wwwDir + toks[1]
        # os.path.exists()  -- checks if that context is valid
        # os.path.isdir()   -- checks if is directory
        try:
            f = open(filename, 'r')
        except IOError as e:
            errCode = errno.errorcode[e.errno]
            if errCode == 'ENOENT':
                reply = 'HTTP/1.1 404 Found\n'
        else:
            if (os.path.isdir(filename)):

            reply = 'HTTP/1.1 200 OK\n'
            # print filename
            mimetype = self.getFileType(filename)
            reply += 'Content-Type: '
            # print mimetype
            reply += mimetype
        print reply
        self.request.sendall(reply)

    def getFileType(self, filename):
        ext = (os.path.splitext(filename))[1]
        if (ext == '.css'):
            return 'text/css'
        if (ext == '.html'):
            return 'text/html'

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
