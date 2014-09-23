#!/usr/bin/python
import socket
import sys
import threading
import time
import datetime
HOSTNAME = 'localhost'
PORT = 3000             # Random port 
BUFFER = 65536

class multiple_clients(threading.Thread):
    def __init__(self,client):
        super(multiple_clients,self).__init__()
        self.client = client

    def receive_data(self):
        try:
            data = self.client.recv(BUFFER)
            return 'Got the message, Thanks..!!'
        except Exception as e:    
            self.client.close()
            return  'Unable to receive the message..!!'

    def send_data(self,data):
        try:
            self.client.send(data)
        except Exception as e:
            self.client.send('Unable to send the data, Check the connection')
            self.client.close()
            return

    def run(self):
        try:
            client_data = self.receive_data()
            if client_data:
                self.client.send(client_data)
        finally:
            pass        
            #self.client.close()      
            
class server_class(threading.Thread):
    def __init__(self):
        super(server_class,self).__init__()
        self.server = None
        self.threads_ = []
         
    def process_data(self):
        client_connection = None               
        message = 'A'*1024 
        print '*'*80
        print 'Server is now running on port %d' % PORT
        print '*'*80

        while True:
            try:
                self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.server.bind((HOSTNAME,PORT))
                self.server.listen(10)  # Listen upto 10 connections before droping them (queue).
                client_connection,client_addr = self.server.accept()
                message_ = ''
                if client_connection:
                    print '\nConnection Received from: %s on port: %d' % (client_addr[0],client_addr[1])
                    server_receive_start = datetime.datetime.now()
                    message_ += client_connection.recv(BUFFER)
                    server_receive_stop = datetime.datetime.now()
                    time_diff = server_receive_stop - server_receive_start
                    print 'The size of the packet received is %d Bytes' % len(message_)
                    print 'The Bandwidth for the server application is %d MBytes/Sec' % (((len(message)/time_diff.microseconds)*(pow(10,6)))/(1024 * 1024))
                    client_connection.close()
                    #multiple_cli = multiple_clients(client_connection)
                    #multiple_cli.setDaemon(True)
                    #thread_ = multiple_cli.start()
                    #self.threads_.append(thread_)
                        
            except Exception as e:
                print '*'*80
                print 'Processing Error..!!'
                print e.message
                print '\nShutting down..!!'
                sys.exit(1)
                raise
                 
            finally:
                self.server.close() 
                #print '*'*80
    def close(self):
        self.server.close()
        
    def run(self):
        self.process_data()

                
if __name__ == '__main__':

    print '*'*80
    print 'Starting Server Daemon..!!'
           
    try:
        server = server_class() 
        server.setDaemon(True)
        server.start()
    except Exception as e:
        print 'Server Stopped'
        print e.message
        print '*'*80
        sys.exit(1)

    try:
        while 1:
            time.sleep(1)
    except Exception as e:
        print e.message
    except KeyboardInterrupt:
        print '*'*78
        print '\nKeyboard Interrupt Caught.!'
        print 'Shutting Down Server..!!!'
        print '*'*80
        sys.exit(1)

    finally:
        server.close()             
