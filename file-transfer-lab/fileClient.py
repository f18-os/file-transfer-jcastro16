#! /usr/bin/env python3

# Echo client program
import sys, params, re, socket

import os
from pathlib import Path

from framedSock import framedSend, framedReceive

sys.path.append("../lib")  # for params

# from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]


def sendFile(fileName):
    print("sending " + fileName + " file")
    dataToSend = "fileName=" + fileName
    framedSend(s, dataToSend.encode(), debug)
    f = open(fileName, "rb").read()
    framedSend(s, f, debug)
    print("received:", framedReceive(s, debug).decode())


if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

fileToSend = "test.txt"

path = Path(os.getcwd() + "/" + fileToSend)
if not path.is_file():
    print("FILE DOES NOT EXIST")
    sys.exit(1)

sendFile(fileToSend)

# print("sending hello world2")
# framedSend(s, b"hello world2", debug)
# print("received:", framedReceive(s, debug))
