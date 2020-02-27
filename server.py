import socket
import threading
import select


#--------------------------------------------------------------------------------------      
def getmessage(client_socket):
    try:
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8")
        return msg

    except:
        return False
#--------------------------------------------------------------------------------------

def sendprivate(username,to_socket,msg):
    try:
        msg = "[Private]" + username +":" + msg
        to_socket.send(bytes(msg,"utf-8"))
        return True

    except:
        return False
#--------------------------------------------------------------------------------------     

if __name__ == "__main__":
    
    print("Starte Main-Thread")

    #Initialize und bind Socket. Dann 
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',1337))
    server_socket.listen(2) #Anzahl der abhörbaren Sockets
    print('Listening for connections on IP:127.0.0.1 Port:1337')

    socket_list = [server_socket]
    username_list =["Server"]
    client_list = {}
    while True:
        #read_sockets hat an erster Stelle falls eine Veränderung eintritt
        read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)

        # Iterate over notified sockets
        for notified_socket in read_sockets:

            # If notified socket is a server socket - new connection, accept it
            if notified_socket == server_socket:

                # Accept new connection
                # That gives us new socket - client socket, connected to this given client only, it's unique for that client
                # The other returned object is ip/port set
                (client_socket,client_address) = server_socket.accept()

                user = getmessage(client_socket)

                #Überspringt diese Schleifenphase
                if user is False:
                    continue

                # Add accepted socket to select.select() list
                socket_list.append(client_socket)
                username_list.append(user)

                # Also save username and username header
                client_list[client_socket] = user

                print("User verbunden über ",client_address,"mit dem Username:",user,"\n")

                message = "Online Users:" + str(username_list)
                #Broadcast an Alle Nutzer                
                for client_sockets in client_list:
                    client_sockets.send(bytes(message,"utf-8"))


            # Else existing socket is sending a message
            else:

                # Receive message
                message = getmessage(notified_socket)
            
                # If False, client disconnected, cleanup
                if message is False:
                    print("User:",client_list[notified_socket],"disconnected ")

                    # Remove from list for socket.socket()
                    socket_list.remove(notified_socket)

                    # Remove from our list of users
                    del client_list[notified_socket]
                    #Alles ab hier überspringen
                    continue
                
                user = client_list[notified_socket]

                # Iterate over connected clients and broadcast message
                for client_socket in client_list:

                    # But don't sent it to sender
                    if client_socket != notified_socket:

                        # Send user and message 
                        message = user + ":" + message + "\n"
                        client_socket.send(bytes(message,"utf-8"))

        # It's not really necessary to have this, but will handle some socket exceptions just in case
        for notified_socket in exception_sockets:

            # Remove from list for socket.socket()
            socket_list.remove(notified_socket)
            username_list.remove(user)

            # Remove from our list of users
            del client_list[notified_socket]
        

    print("Beende Main-Thread")