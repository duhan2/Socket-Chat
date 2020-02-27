import socket
import threading

class handler_thread(threading.Thread):

    def __init__(self,client_socket,server_addr,operation):
       
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.server_addr = server_addr
        self.operation = operation

        
    def run(self):
        
        if self.operation == "read":   

            while True:

                rcv = self.client_socket.recv(1024)
                rcv = rcv.decode("utf-8")
                print(rcv,"\n")


        if self.operation == "write":

            #print("Benutzen Sie folgendes Format für ihre Nachrichten [IP-Adresse des Clients/all :][Nachricht]\n")
            print("Schreiben Sie \"Server:quit\" zum beenden\n")

            while True:
                
                message = input("Ihre Eingabe?\n")
                
                if message == "Server:quit":
                    self.client_socket.send(bytes(message,"utf8"))
                    print("Schleife wird beendet")
                    break

                self.client_socket.send(bytes(message,"utf8"))




if __name__ == "__main__":

    print("Starte Main-Thread")

    #Initialisieren des sockets
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    #Tupel für Server
    server_addr = ('127.0.0.1', 1337)
    #Verbindung zum Server
    client_socket.connect(server_addr)

    msg = input("Enter Username first\n")
    client_socket.send(bytes(msg,"utf8"))

    reading_handler = handler_thread(client_socket,server_addr,"read")
    writing_handler = handler_thread(client_socket,server_addr,"write")

    reading_handler.start()
    writing_handler.start()
    
    #print("Beende Main-Thread")