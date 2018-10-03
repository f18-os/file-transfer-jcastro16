#! /usr/bin/env python3
import os
from pathlib import Path

import time

import params
import socket
import sys

sys.path.append("../lib")       # for params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)

while True:
    print("Server is running... %d", os.getpid())
    sock, addr = lsock.accept()

    pid = os.fork()

    if pid == 0:
        # child
        print("(CHILD) connection rec'd from", addr)
        from framedSock import framedSend, framedReceive

        fileName = "N/A"

        while True:
            payload = framedReceive(sock, debug)
            time.sleep(10)

            if not payload:
                print("(CHILD) Ending connection with client")
                sock.close()
                sys.exit(0)

            payLoadString = payload.decode()
            print("(CHILD) Payload in str " + payLoadString)

            if payLoadString.startswith("fileName="):
                fileName = payLoadString.split("=")[1]
                print("(CHILD) received file name " + fileName)

                path = Path(os.getcwd() + "/serverFiles/" + fileName)
                if path.is_file():
                    payload = b"FILE ALREADY EXISTS ON SERVER!"  # make emphatic!
                    framedSend(sock, payload, debug)
                    print("(CHILD) (FILE ALREADY EXISTS) Ending connection with client")
                    sock.close()
                    sys.exit(0)

                continue
            elif payload:
                print("(CHILD) rec'd: ", payload)
                f = open(os.getcwd() + "/serverFiles/" + fileName, "wb")
                f.write(payload)

            payload = b"Server received file"  # make emphatic!
            framedSend(sock, payload, debug)
            sock.close()
            sys.exit(0)
    else:
        # parent just keep listening for connections
        pass
