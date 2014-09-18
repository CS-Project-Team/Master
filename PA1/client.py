#!/usr/bin/python
import socket
import sys
from datetime import datetime
import threading
SERVER_HOST = 'localhost'
SERVER_PORT = 3000
BUFFER = 1024
SEND_TIMES = []
RECEIVE_TIMES = []

class client(threading.Thread):
    def __init__(self):
        super(client,self).__init__()
        self.client = None
        self.server_addr = (SERVER_HOST,SERVER_PORT)
        self.packet = 'Hello'
    
    def send_data(self,data):
        try:
            start_packet_time = datetime.now() 
            self.client.send(data)
            stop_packet_time = datetime.now()
        except Exception as e:
            print 'Could not send the data.!!'
            print e.message
            print '*'*80
            self.client.close()
            return
                
        return (stop_packet_time - start_packet_time)
    
    def receive_data(self):
        try:
            start_packet_time = datetime.now()
            data = self.client.recv(BUFFER)  
            stop_packet_time = datetime.now()
        except Exception as e:
            print 'Could not receive the data'
            print e.message
            print '*'*80
            self.client.close()
            return
                
        return (data,(stop_packet_time - start_packet_time))  
            
    def process_data(self,data):
        try:
            self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.client.connect(self.server_addr)
            send_time = self.send_data(data)
            receive_time = self.receive_data()
            SEND_TIMES.append(send_time)
            RECEIVE_TIMES.append(receive_time)

        except Exception as e:
            print 'Cannot connect to the server..!!'
            print 'Check the connection parameters' 
            print e.message
            print '*'*80
            sys.exit(1)
               
        finally:
            self.client.close()
        
        print 'The time taken to send data:',send_time
        print 'The time taken to receive data:',receive_time
        
    def run(self):
        try:
            self.process_data(self.packet)
        except Exception as e:
            print 'Error processing the data..!!'
            print e.message
            sys.exit(1)    

if __name__ == '__main__':
    cli = client()
    cli.start()
    cli.join() 
