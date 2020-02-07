#!/usr/bin/env python3
# coding: utf-8
# Copyright 2016 Abram Hindle, https://github.com/tywtyw2002, and https://github.com/treedust
# Copyright 2020 Hyeon Yu
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

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib.parse

def help():
    print("httpclient.py [GET/POST] [URL]\n")


#It’s a good idea to send the Host header in a GET or POST
class HTTPResponse(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        return None

    def get_code(self, data):
        return int(data.split()[1])

    def get_headers(self,data):
        return data.split("\r\n\r\n")[0]

    def get_body(self, data):
        return data.split("\r\n\r\n")[1]
    
    def sendall(self, data):
        self.socket.sendall(data.encode('utf-8'))
        
    def close(self):
        self.socket.close()

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return buffer.decode('utf-8')

    def GET(self, url, args=None):
        o = urllib.parse.urlparse(url)
        path = o.path
        hostname = o.hostname

        port = o.port
        if (port == None):
            port = 80
        
        if (path == ""):
            path = "/"
        get_request = "GET " + str(path) + " HTTP/1.1\r\n" + "Host: " + str(hostname) + "\r\n" + "Accept: */*\r\nConnection: Close\r\n\r\n"
        
        self.connect(hostname, port)
        self.sendall(get_request)
        
        recieved = self.recvall(self.socket)
        code = self.get_code(recieved)
        body = self.get_body(recieved)

        self.close()

        print(body)
        return HTTPResponse(code, body)

    def POST(self, url, args=None):
        o = urllib.parse.urlparse(url)
        path = o.path
        hostname = o.hostname
        port = o.port
        content_length = 0

        if (port == None):
            port = 80
        
        if (path == ""):
            path = "/"

        if (args != None):
            content_length = len(urllib.parse.urlencode(args))
            post_request = "POST " + str(path)+ " HTTP/1.1\r\n" + "Accept: */*\r\nHost: " + str(hostname) + "\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n" + "Content-Length: " + str(content_length) + "\r\n" + "Connection: close\r\n\r\n" + urllib.parse.urlencode(args)
        else:
            post_request = "POST " + str(path)+ " HTTP/1.1\r\n" + "Accept: */*\r\nHost: " + str(hostname) + "\r\n" + "Content-Type: application/x-www-form-urlencoded\r\n" + "Content-Length: " + str(content_length) + "\r\n" + "Connection: close\r\n\r\n"

        self.connect(hostname, port)
        self.sendall(post_request)

        recieved = self.recvall(self.socket)
        code = int(self.get_code(recieved))
        body = self.get_body(recieved)

        self.close()

        print(body)
        return HTTPResponse(code, body)

    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print(client.command( sys.argv[2], sys.argv[1] ))
    else:
        print(client.command( sys.argv[1] ))
