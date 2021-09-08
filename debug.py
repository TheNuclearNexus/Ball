from typing import List
from helper import getGridString, getMemoryString, createGrid
from socketserver import *
import socket
import json
import time
import threading
import os
import sys

HOST, PORT = "localhost", 9999

syncData = {
    'grid': '',
    'balls': [],
    'memory': []
}

init = True 

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
        
        global init
        if init:
            syncData["init"] = True
            init = False
        else:
            syncData["init"] = False

        if data["type"] == 'sync':
            syncData["init"] = True
            self.request.send(bytes(json.dumps(syncData), 'ascii'))
        elif data["type"] == 'update':
            self.request.send(bytes(json.dumps(syncData), 'ascii'))
        else:
            self.request.send(b'Invalid Type')
        return

    def finish(self):
        return BaseRequestHandler.finish(self)

class DebugServer(TCPServer):
    pass

debugServer = None
def __startServer():
    # Create the server, binding to localhost on port 9999
    with DebugServer((HOST, PORT), DebugHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        global debugServer
        debugServer = server
        print('Server started')
        debugServer.serve_forever()
        
thread = None
def startServer():
    global thread
    thread = threading.Thread(target=__startServer)
    thread.start()
def stopServer():
    debugServer.shutdown()
    

class RequestType:
    SYNC = 'sync'
    UPDATE = 'update'

class Client:
    def request(self, type: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((HOST, PORT))
                sock.sendall(bytes(json.dumps({'type':type}), 'ascii'))
                response = str(sock.recv(1024*64), 'ascii')
                return json.loads(response)
            except Exception as err:
                print('Waiting...', '',end='\r')
                return None

    def __init__(self):
        syncData = self.request(RequestType.SYNC)
        self.syncData = syncData
        self.grid = []

    def update(self):
        syncData = self.request(RequestType.UPDATE)
        if syncData != None and syncData != self.syncData:
            self.syncData = syncData

            if syncData["init"] == True:
                self.grid = createGrid(syncData["grid"])

            os.system("cls")
            content = getGridString(self.grid, syncData["balls"])

            content += '\n\n\n\n'
            content += getMemoryString(syncData["memory"], syncData["pointers"])

            lineCount = len(content.split('\n')) 
            # print('\n'*lineCount*4)
            sys.stdout.write(content + ('\r'*(lineCount)))
            sys.stdout.flush()




if __name__ == '__main__':
    c = Client()
    while True:
        c.update()
        time.sleep(1/120)