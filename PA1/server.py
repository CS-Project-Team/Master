#!/usr/bin/python
import socket
import sys
import threading
HOSTNAME = 'localhost'
PORT = 3000             # Random port 
BUFFER = 1024

# Handling Multiple Clients
class multiple_clients(threading.Thread):
    def __init__(self,client):
        super(multiple_clients,self).__init__()
        self.client = client

    def receive_data(self):
        data = self.client.recv(1024)
        print 'The following data was recieved:',data

    def send_data(self,data):
        self.client.send(data)

    def run():
        client_data = self.receive_data()
        if client_data:
            data_to_send = [None]*1024
            self.client.send(data_to_send)
        self.client.close()      
            

class server_class():
    def __ini__(self):
        # Creating a TCP socket which can be reusable.
        try:
            self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((HOSTNAME,PORT))
            self.server.listen(10)  # Listen upto 10 connections before droping them (queue).
            print '*'*80
            print 'Server is now running on port %d' % PORT
            print '*'*80

        except Exception as e:
            print 'Error Create the Socket'
            print e
            sys.exit(1)
        
    def process_data(self):
        client_connection = None
        while True:
            try:
                client_connection,client_addr = self.server.accept()
                if client_connection:
                    print 'Connection Received from: %s' % client_addr
                    multiple_cli = multiple_clients(client_connection)
                    mutiple_cli.start()
                    multiple_cli.join
                    
            except KeyboardInterrupt:
                sys.exit
                
if __name__ == '__main__':
    s = server_class() 
    s.process_data()                                                  
