#!/usr/bin/env python3
import socket
import time
import sys

#create a tcp socket
def create_tcp_socket():
    print('Creating socket')
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except (socket.error, message):
        print(f'Failed to create socket. Error code: {str(message[0])} , Error message : {message[1]}')
        sys.exit()
    print('Socket created successfully')
    return s

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload)
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")

def main():
    try:
        #Serve connections
        #make the socket
        s = create_tcp_socket()

        #define address & buffer size
        server_host = ""
        server_port = 8001
        server_buffer_size = 4096
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((server_host, server_port))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            #Connect to Google
            #define address info, and buffer size
            client_host = 'www.google.com'
            client_port = 80

            #make the socket, get the ip, and connect
            s_google = create_tcp_socket()

            remote_ip = get_remote_ip(client_host)

            s_google.connect((remote_ip , client_port))
            print (f'Socket Connected to {client_host} on ip {remote_ip}')
            
            #receive data, wait a bit, then send it to google
            full_data = conn.recv(server_buffer_size)
            time.sleep(0.5)
            send_data(s_google, full_data)

            #receive google's response
            google_data = b""
            while True:
                data = s_google.recv(server_buffer_size)
                if not data:
                    break
                google_data += data

            #send google's response back to our client
            conn.sendall(google_data)
            conn.close()
        
    except Exception as e:
        print(e)
    finally:
        #always close at the end!
        s.close()
        s_google.close()


if __name__ == "__main__":
    main()