import socket
import threading

class handler_thread(threading.Thread):

    def __init__(self,client_socket,server_addr,operation):
       
        threading.Thread.__init__(self)
        
        self.client_socket = client_socket
        self.server_addr = server_addr
        self.operation = operation

        


    def run(self):
        
        if self.operation == 1:   

            while True:

                rcv = self.client_socket.recv(1024)
                rcv = rcv.decode("utf-8")
                print("Recieved Message: ",rcv,"\n")


        if self.operation == 2:

            #print("Benutzen Sie folgendes Format für ihre Nachrichten [IP-Adresse des Clients/all :][Nachricht]\n")
            print("Schreiben Sie quit zum beenden")

            while True:
                
                message = input("Ihre Eingabe?\n")
                
                if message == 'quit':
                    print("Schleife wird beendet")
                    break

                self.client_socket.send(bytes(message,"utf8"))



if __name__ == "__main__":

    print("Starte Main-Thread")

    #init UDP Socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    
    server_addr = ('127.0.0.1', 1337)

    client_socket.connect(server_addr)

    reading_handler = handler_thread(client_socket,server_addr,1)
    writing_handler = handler_thread(client_socket,server_addr,2)

    reading_handler.start()
    writing_handler.start()
    
    print("Beende Main-Thread")