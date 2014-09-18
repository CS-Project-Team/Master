#!/usr/bin/python
import socket
import sys
import threading
HOSTNAME = 'localhost'
PORT = 3000             # Random port 
BUFFER = 1024

class multiple_clients(threading.Thread):
    def __init__(self,client):
        super(multiple_clients,self).__init__()
        self.client = client

    def receive_data(self):
        try:
            data = self.client.recv(1024)
            print 'The following data was recieved:',data
        except Exception as e:    
            print 'Unable to receive the message..!!'
            self.client.close()
            return

    def send_data(self,data):
        try:
            self.client.send(data)
        except Exception as e:
            print 'Unable to send the data, Check the connection'
            self.client.close()
            return

    def run(self):
        try:
            client_data = self.receive_data()
            if client_data:
                #data_to_send = [None]*1024
                data_to_send = 'Got the message, Thanks..!!'
                self.client.send(data_to_send)
        finally:        
            self.client.close()      
            

class server_class():
    def __init__(self):
        self.server = None
        self.threads = []
         
    def process_data(self):
        client_connection = None
        while True:
            try:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind((HOSTNAME,PORT))
                self.server.listen(10)  # Listen upto 10 connections before droping them (queue).
                print '*'*80
                print 'Server is now running on port %d' % PORT
                print '*'*80

                client_connection,client_addr = self.server.accept()

                if client_connection:
                    print 'Connection Received from: %s on port: %d' % (client_addr[0],client_addr[1])
                    multiple_cli = multiple_clients(client_connection)
                    thread = multiple_cli.start()
                    self.threads.append(thread)
                    multiple_cli.join()
                       
            except KeyboardInterrupt:
                print '*'*80
                print '\nKeyboard Interrupt Caught.!'
                print 'Shutting Down Server..!!!'
                sys.exit(1)
           
            except Exception as e:
                print '*'*80
                print 'Processing Error..!!'
                print e.message
                print '\nShutting down..!!'
                sys.exit(1)
           
            finally:
                self.server.close()     
                print '*'*80     
                
if __name__ == '__main__':
    s = server_class() 
    s.process_data()                                                  
