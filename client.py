import socket
import threading

class handler_thread(threading.Thread):
    #Global damit beide Threads beim Reconnecten drauf zugreifen
    client_socket = 0

    def __init__(self,client_socket,server_addr,operation,username):
       
        threading.Thread.__init__(self)
        
        self.server_addr = server_addr
        self.operation = operation
        self.new_clientsocket = 0
        self.username = username

        handler_thread.client_socket = client_socket
        
    def run(self):
        
        if self.operation == "read":   

            while True:

                rcv = handler_thread.client_socket.recv(1024)
                rcv = rcv.decode("utf-8")
                print(rcv,"\n")

                #Wenn Server Leerstring sendet, ist er abgestürzt
                if not len(rcv):
                    handler_thread.client_socket.close()
                    print("Server abgestuerzt. Verbinde neu\n")
                    handler_thread.client_socket = reconnect(self.new_clientsocket,('127.0.0.2',1338))
                    handler_thread.client_socket.send(bytes(self.username,"utf8"))
                    print("Geben Sie erneut ihren Username ein")
                    continue
                    
        

        if self.operation == "write":

            print("Syntax fuer spezifische Nachrichten ist folgende: [Username]:[Nachricht]\n")
            print("Fuer einen Broadcast schreiben Sie \"Broadcast\" an die Stelle des Usernames\n")
            #print("Fuer eine Liste mit Serverinteraktionen, schreiben Sie \"Server:help\" \n")

            while True:
                
                message = input("Ihre Eingabe?\n")
                
                handler_thread.client_socket.send(bytes(message,"utf8"))

#-----------------------------------------------------------------------------------------------------------------

def reconnect(client_socket,server_addr):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    client_socket.connect(server_addr)
    return client_socket


if __name__ == "__main__":

    print("Starte Main-Thread")
    try:
        #Initialisieren des sockets
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #Tupel für Server
        server_addr = ('127.0.0.1', 1337)
        #Verbindung zum Server
        client_socket.connect(server_addr)
    except:
        print("Couldn't connect\n")
        server_addr = ('127.0.0.2',1338)
        client_socket.connect(server_addr)

    msg = input("Enter Username first\n")
    username = msg
    client_socket.send(bytes(msg,"utf8"))

    reading_handler = handler_thread(client_socket,server_addr,"read",username)
    writing_handler = handler_thread(client_socket,server_addr,"write",username)

    reading_handler.start()
    writing_handler.start()
    
    #print("Beende Main-Thread")
