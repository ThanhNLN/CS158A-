# Le Ngoc Thanh Nguyen
# CIS 41B - Lab 5: a simulation of a low-level client-server application
# File: client

import socket
import pickle

class Client:
    '''Client'''
    HOST = 'localhost'
    PORT = 5551
    TIME_OUT = 2
    def __init__(self):

        try:
            with socket.socket() as self.S:
                self.S.connect((self.HOST, self.PORT))
                self.S.settimeout(self.TIME_OUT)
                print("Client connect to:", self.HOST, "port:", self.PORT)
                self.run()
                self.endProgram()
        except socket.timeout:
            print("No response from server")
            raise SystemExit
        except ConnectionError:
            print("Cannot connect to server")
            raise SystemExit

    def run(self):
        '''Let user run the program'''
        methodTable = {'c': self.changeDir,
                       'l': self.listDir,
                       'f': self.createFile,
                       'q': self.endProgram}
        self.currentDir()
        self.requestList()
        choice = input("Enter choice: ")
        while choice != 'q':
            try:
                methodTable[choice.lower()]()
                self.requestList()
                choice = input("Enter choice: ")
            except KeyError:
                print("Invalid input. Available choices are", ','.join(methodTable.keys()))
                choice = input("Enter choice: ")
                if choice.lower() == 'q':
                    self.endProgram()

    def requestList(self):
        '''List all available request'''
        menu = "c: change directory \nl: list directory \nf: create file \nq: quit"
        print(menu)

    def currentDir(self):
        '''Request current working directory'''
        self.S.send(pickle.dumps(['g']))
        self.currentDir = pickle.loads(self.S.recv(1024))
        print("Current Directory:", self.currentDir)
        print()

    def endProgram(self):
        '''End program'''
        print("Ending program\n")
        self.S.send(pickle.dumps(['q']))
        self.S.close()
        #raise SystemExit
    def listDir(self):
        '''List directory'''
        self.S.send(pickle.dumps(['l']))
        fromServer = pickle.loads(self.S.recv(1024))
        if len(fromServer) == 0:
            print("empty directory" )
        else:
            print("Directories and files found under ", self.currentDir)
            for item in fromServer:
                print(item)
        print()
    def changeDir(self):
        '''Change Directory'''
        path = input("Enter path, starting from current directory:")
        self.S.send(pickle.dumps(['c', path]))
        fromServer = pickle.loads(self.S.recv(1024))
        print(fromServer)
        print()

    def createFile(self):
        '''Create new empty file'''
        fileName = input("Enter file name: ")
        self.S.send(pickle.dumps(['f', fileName]))
        fromServer = pickle.loads(self.S.recv(1024))
        print(fromServer)
        print()

if __name__ == '__main__':
    Client()