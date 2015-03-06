'''
Created on Feb 14, 2015

A simple TCP client using sockets.

@author: Haley Garrison
'''
from socket import socket, AF_INET, SOCK_STREAM

class Tcp_client:
    '''
    This class is capable of creating a tcp connection with a given host name and port number.
    Strings can then be sent through the connection. or read from the connection.
    '''
    CHUNK_SIZE = 1024
    TIMEOUT = 5
    
    def __init__(self, host, port):
        '''
        Initiates the connection to host:port
        '''
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.settimeout(Tcp_client.TIMEOUT)
        self.socket.connect((host, port))
    
    def write(self, data):
        '''
        Writes data to the tcp connection
        '''
        self.socket.sendall(data)
    
    def read(self, length=-1):
        '''
        Reads and returns data up to the maximum given length or all data available if 
        length is -1.  This method is blocking.
        '''
        data = ''
        if length != -1:
            data = self.socket.recv(length)
        else:
            # Keep getting chunks of data until there is no more
            chunk = self.socket.recv(Tcp_client.CHUNK_SIZE)
            data += chunk
            while len(chunk) == Tcp_client.CHUNK_SIZE:
                chunk = self.socket.recv(Tcp_client.CHUNK_SIZE)
                data += chunk
            
        # Return the data that was read
        return data
    
    def close(self):
        '''
        Closes this tcp connection
        '''
        self.socket.close()