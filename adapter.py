
#*************************Project developed in flask framework*****************

import socket               # Import socket module
import threading            # Import Thread module
import time

#********* TCP socket at port 4444 and ip=127.0.0.1 for sending and receiving data
def seversocket():
    import socket
    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serv.bind(('127.0.0.1', 4444))
    serv.listen(5)
    while True:

        print ("Waiting for clients. . .")
        conn, addr = serv.accept()
        print ("Got connection from:", addr)
        while True:

            data = conn.recv(4096)

            #data[:].decode("utf-8")
            if not data: break
            Rdata=data[:].decode("utf-8")

            if(Rdata[9:11] == "01"):                        # login packet
                print("[REQUEST]: Login")
                login_response="78 78 05 01 00 05 9F F8 0D 0A"
                login_response_byte=login_response.encode()
                conn.send(login_response_byte)
            elif(Rdata[9:11] =="23"):                      #Heartbeat packet
                print("[REQUEST]: Heartbeat")
                heartbeat_response="78 78 05 23 01 00 67 0E 0D 0A"
                heartbeat_response_byte=heartbeat_response.encode()
                conn.send(heartbeat_response_byte)
            elif(Rdata[9:11] =="22"):                     #GPS packet
                print("[REQUEST]: GPS")
                gps_response="78 78 05 22 01 00 67 0E 0D 0A"
                gps_response_byte=gps_response.encode()
                conn.send(gps_response_byte)
        conn.close()
        print("Client Disconnected!")


# main driver function
if __name__ == '__main__':
    threads=[]
    print("=========================================")
    print("             Concox Adaptor")
    print("=========================================")
    new_thread=threading.Thread(target=seversocket)
    new_thread.start()
    threads.append(new_thread)
    for thread in threads:
        thread.join()
