from typing import List
from helper import getGridString, getMemoryString
from socketserver import *
import socket
import json
import time
import threading
import os

HOST, PORT = "10.48.124.248", 42069

syncData = {
    'grid': [],
    'balls': [],
    'memory': []
}
def setSyncData(data):
    global syncData
    syncData = data
class DebugHandler(BaseRequestHandler):
    
    def __init__(self, request, client_address, server):
        BaseRequestHandler.__init__(self, request, client_address, server)
        return

    def setup(self):
        return BaseRequestHandler.setup(self)

    def handle(self):

        # Echo the back to the client
        data = json.loads(self.request.recv(1024))
        
        if data["type"] == 'sync':
            self.request.send(bytes(json.dumps(syncData), 'ascii'))
        else:
            self.request.send(b'Invalid Type')
        return

    def finish(self):
        return BaseRequestHandler.finish(self)

class DebugServer(TCPServer):
    pass

def __startServer():
    # Create the server, binding to localhost on port 9999
    with DebugServer((HOST, PORT), DebugHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        print('Server started')
        server.serve_forever()
thread = None
def startServer():
    global thread
    thread = threading.Thread(target=__startServer)
    thread.start()


class RequestType:
    SYNC = 'sync'
    UPDATE = 'update'

class Client:
    def request(self, type: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((HOST, PORT))
                sock.sendall(bytes(json.dumps({'type':type}), 'ascii'))
                response = str(sock.recv(1024*16), 'ascii')
                return json.loads(response)
            except Exception as err:
                print('Waiting...', '',end='\r')
                return None
    def __init__(self):
        syncData = self.request(RequestType.SYNC)

    def update(self):
        syncData = self.request(RequestType.SYNC)
        if syncData != None:
            os.system("cls")
            print('\n'*50)
            content = getGridString(syncData["grid"], syncData["balls"])
            content += '\n\n\n\n'
            content += getMemoryString(syncData["memory"], syncData["pointers"])

            print(content, '', end='\r'*(len(content.split('\n'))))




if __name__ == '__main__':
    c = Client()
    while True:
        c.update()
        time.sleep(1/30)