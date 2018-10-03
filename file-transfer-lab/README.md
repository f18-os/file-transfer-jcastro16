

# File-Transfer Lab

**Purpose:**

A Server/Client program that grants the ability to transfer files from client to server. This is managed by the client sending a copy of the file to the server. The assignment is to write fileClient.py and fileServer.py which can transfer a file from a client to the server. The programs should:

- be in the file-transfer-lab subdir

    both fileClient.py and fileSever.py will be located under directory &quot;file-transfer-lab&quot;

- work with and without the proxy

    works well without proxy

- support multiple clients simultaneously using fork()

    achieved under the fileserver, this allows to fork a child, so the parent server is still running while waiting for incoming connections.

   # How to test for fork()

    Instead of creating a large file, my method was to sleep the process for 10 seconds and run multiple clients on the same server. Every time a client connected, it will fork and the server process still runs until the server is terminated.

- gracefully deal with scenarios such as:
  - zero length files – file must contain data at and not be empty
  - user attempts to transmit a file which does not exist -program will alert the user if the file that is to be transmitted doesn&#39;t exist, it will display &quot;FILE DOES NOT EXIST&quot;, coming from Client
  - file already exists on the server – program will alert the user if the file that is to be transmitted exists, it will display &quot;FILE ALREADY EXIST ON SERVER&quot;, coming from Server.
  - the client or server unexpectedly disconnect – notify if the server is no longer available. Sleep the process and quit sever. (Not done, currently in progress)





# **Using the Program**

NOTE: Its best to be ran through an IDE similar to PyCharm as the program was constructed using PyCharm.

As any other program, execute fileServer.py to initiate server, then run fileClient.py. If client is ran without server being run first, program will crash. Server must run first.

After server has started, multiple print comments will show the user as to what the program is doing. After, all the requirements above can be tested. A test file has been provided for testing purposes. More files can be created if desired to test different functionalities.



# **Files in Directory**

fileClient.py – contains function that allows the client(s) to sendFile. This is accomplished by grabbing the string data and converting it to binary data with &quot;rb&quot; and sending it to the serer. In this class, code line #70 is major part of the program that allows to name which file is to be sent to the sever side. It also notifies if the &quot;FILE DOES NOT EXIST&quot;

fileServer.py – sets the server, listens to port # and establish connection if clients try to connect. This is also responsible for the fork() to allow multiple clients to connect to same server. Method to check if &quot;file already exists on server&quot; is cover here as well.

framedSock.py - holds the starter code provided by Dr. Freudenthal that enables the framed send and receive.

params.py – provided by Dr. Freudenthal in the &quot;framed-echo&quot; repo, which most of the  re-used code for this project was extracted from.

test.txt – file for testing purposes within the IDE. Being able to modify, create and delete

files if needed for different test cases scenarios.



