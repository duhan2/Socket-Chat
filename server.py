import socket
import threading

class client_thread(threading.Thread):

    def __init__(self,union):
       
        threading.Thread.__init__(self)

        (client_socket,addr) = union
        (ipaddr,portno) = addr

        print("Client verbunden mit IP-Adresse:",ipaddr," und Portnummer:",portno,"\n")

        self.client_socket = client_socket
        self.addr = addr
        self.ipaddr = ipaddr
        self.portno = portno
    
    def run(self):
        #print("Starte Client_Thread mit Addr",self.addr)

        while True:
            
            msg = client_socket.recv(1024)
            msg = msg.decode("utf-8")


            print("Message from Client_Address[",self.ipaddr,"]:",msg)

            client_socket.send(bytes("[Server]: Forwarded your message","utf-8"))
            

        #print("Beende Client_Thread mit Addr",self.ipaddr)



if __name__ == "__main__":
    
    print("Starte Main-Thread")

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',1337))
    server_socket.listen(2)

  

    while True:

        (client_socket,addr)= server_socket.accept()

        ct = client_thread((client_socket,addr))

        ct.start()
        

    print("Beende Main-Thread")