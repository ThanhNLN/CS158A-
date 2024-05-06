# CS158A: Server - Client Application

## Overview
This program implements a low-level client-server application in Python using sockets. The application consists of two components: a server and a client. 
The server is capable of handling multiple client connections concurrently. 
Clients can interact with the server to perform various file system operations such as listing files and directories, changing directories, and creating files.


## Files
server.py: Contains the code for the server component of the application.
client.py: Contains the code for the client component of the application.


## Dependencies
This program requires Python 3.12 to be installed on the system.


## How to Run

Open a terminal window.
Navigate to the directory containing the program files.
Start the server by running the following command:
    ```sh
    python server.py [num_clients] [timeout]
    ```
    > Replace [num_clients] with the desired number of clients the server can respond to.
    > Replace [timeout] with the timeout time for the server's listening socket (in seconds).

Open another terminal window.
Navigate to the directory containing the program files.
Start the client by running the following command:

    ```sh
    python client.py [server_port]
    ```
    > Replace [server_port] with the port number on which the server is listening.


## Usage

Upon connecting to the server, the client can request and receive the current directory from the server.
The client can then choose from the following options:
    c: Change directory
    l: List directory contents
    f: Create a new file
    q: Quit the program

The client sends each request as a single message to the server and displays the server's response for each request.


## Future Features

* Authentication and Authorization: Implement user authentication and authorization mechanisms to control access to server resources.
* File Transfer: Allow clients to upload and download files to and from the server.
* Error Handling: Improve error handling to provide more informative error messages to clients.
* Command History: Maintain a history of commands executed by clients for auditing and replaying purposes.
* Directory Navigation: Enhance directory navigation capabilities by supporting relative paths, path completion, etc.
* Real-time Updates: Enable real-time updates for clients, such as notifying clients when new files are created or when directories are modified.
* Remote Execution: Allow clients to execute arbitrary commands on the server and receive the output.
* Bandwidth Throttling: Implement bandwidth throttling to limit the rate of data transfer between the server and clients.
