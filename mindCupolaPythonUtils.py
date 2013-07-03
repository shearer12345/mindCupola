'''
Created on 23 Jul 2012

@author: shearer
'''
import inspect
import socket, struct

def whoAmI():
    return inspect.stack()[1][3]

def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def get_default_gateway_linux():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))
