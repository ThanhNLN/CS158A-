# SJSU - CS158A
# Project: TCP server-client 
# Author: Le Ngoc Thanh Nguyen and Annie Luu
# Server component of the application.

import os
import sys
import socket
import pickle
import threading
class Server:
    '''Server'''
    _HOST = "localhost"
    _PORT = 5551
    MIN_USER = 1
    MAX_USER = 4
    MIN_TIME_OUT = 3
    MAX_TIME_OUT = 30

    def __init__(self,userNum,timeOut):
        if not (self.evaluateInput(userNum, self.MIN_USER, self.MAX_USER)
                and self.evaluateInput(timeOut, self.MIN_TIME_OUT, self.MAX_TIME_OUT)):
            print("Invalid input. Exiting program")
            raise SystemExit
        self.runServer(timeOut,userNum)

    def evaluateInput(self, num, minNum, maxNum):
        '''Evaluate number input within the [minNum,maxNum] range.'''
        validChoice = False
        if minNum <= num <= maxNum:
            validChoice = True
        return validChoice

    def runServer(self,timeOut,clientNum):
        '''Create and run the server'''
        with socket.socket() as self.S :
            self.S.bind((self._HOST, self._PORT))
            print("Server is up, hostname:", self._HOST, "port:", self._PORT)

            self.S.listen()             # listen is blocking, has loop to keep listening
            self.S.settimeout(timeOut)  # interupt from user/terminal force stop return -1, code stop on purpose cause 1

            self.curDirectories = {}
            threads = []
            for i in range(clientNum):
                thread = threading.Thread(target=self.processClient)
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
                # print(thread.is_alive()) # debug
            print("All clients disconnected. Ending program")
            
    def processClient(self):
        '''Let client run the program'''
        try:
            (conn, addr) = self.S.accept()
            print("Connecting to client at port:", conn.getsockname()[1])
            self.fromClient = pickle.loads(conn.recv(1024))
            # self.testPrint(addr, self.fromClient)
            self.curDirectories[threading.current_thread().name] = os.getcwd()
            methodTable = {'pwd': self.getCurrentDir,
                           'cd': self.changeDir,
                           'ls': os.listdir,
                           'touch': self.createFile,
                           'mkdir': self.makeDirectory,
                           'rmdir': self.removeDir,
                           'rm': self.removeFile }

            while self.fromClient[0] != 'q':
                self.oriDir()
                response = methodTable[self.fromClient[0].lower()]()
                # print(response)         #debug
                conn.send(pickle.dumps(response))
                self.fromClient = pickle.loads(conn.recv(1024))
        except socket.timeout:
            print("timed out")

    def testPrint(self, ad, prompt):
        print("From client:", ad)
        print("Received:", prompt)

    def oriDir(self):
        '''Move to original directory'''
        if os.getcwd() != self.curDirectories[threading.current_thread().name]:
            os.chdir(self.curDirectories[threading.current_thread().name])

    def getCurrentDir(self):
        '''Return the current directory path'''
        curDir = os.getcwd()
        print("Sending", curDir)
        return curDir

    def changeDir(self):
        '''Move to another directory'''
        path = self.fromClient[1]
        try:
            os.chdir(path)
            newPath = os.getcwd()
            self.curDirectories[threading.current_thread().name] = newPath
            return 'New path: ' + newPath
        except OSError:
            return 'Invalid path'

    def listFileInDir(self):
        '''Return list of subdirectory and file names in current directory'''
        return os.listdir()

    def createFile(self):
        '''Create and empty, new file'''
        fileName = self.fromClient[1]

        #if os.path.isfile(fileName):
        if os.path.exists(fileName):            # check both file and folder names
            return 'File or folders already exists'
        else:
            # cm = 'touch ' + fileName          #use for MAC/Linux
            # os.system(cm)                     #use for MAC/Linux
            f = open(fileName, 'a')
            f.close()
            return 'File created in ' + os.getcwd()
        
    def makeDirectory(self):
        '''Create a new directory'''
        dirName = self.fromClient[1]
        
        if os.path.exists(dirName):
            return 'Directory already exists'
        else:
            try:
                os.makedirs(dirName)
                return f'Directory {dirName} created'
            except OSError as e:
                return f'Error creating directory: {e}'
        
    def removeFile(self):
        '''Remove an existing file'''
        fileName = self.fromClient[1]
        
        if not os.path.exists(fileName):
            return 'File does not exist'
        elif os.path.isdir(fileName):
            return 'Path is a directory, not a file'
        else:
            try:
                os.remove(fileName)
                return f'File {fileName} removed'
            except OSError as e:
                return f'Error removing file: {e}'
            
    def removeDir(self):
        '''Remove an existing directory'''
        dirName = self.fromClient[1]
        
        if not os.path.exists(dirName):
            return 'Directory does not exist'
        elif not os.path.isdir(dirName):
            return 'Path is not a directory'
        else:
            try:
                os.rmdir(dirName)
                return f'Directory {dirName} removed'
            except OSError as e:
                return f'Error removing directory: {e}'
            
if __name__ == '__main__':
    try:
        userNum = int(sys.argv[1])
        timeOut = int(sys.argv[2])
    except (ValueError, IndexError):
        print("Invalid input. Exiting program")
        raise SystemExit
    Server(userNum,timeOut)