import socket
import threading

class client_thread(threading.Thread):

    def __init__(self,union,all_clients):
       
        threading.Thread.__init__(self)

        (client_socket,addr) = union
        (ipaddr,portno) = addr

        print("Client verbunden mit IP-Adresse:",ipaddr," und Portnummer:",portno,"\n")

        self.client_socket = client_socket
        self.addr = addr
        self.ipaddr = ipaddr
        self.portno = portno
        self.all_clients = all_clients
    
    def run(self):
        #print("Starte Client_Thread mit Addr",self.addr)

        while True:
            
            msg = client_socket.recv(1024)
            msg = msg.decode("utf-8")


            i = 0

            for c in msg:

                if c == ':':
            
                    break

                i = i+1

            #print("Eingegangene MEssage:",msg[0:i])

            checkvalue = checkfor(msg[0:i],self.all_clients)

            if checkvalue == False:
                print("No ipadress found\n")
            else:
                (destclient_socket,destclient_addr) = checkvalue
                destclient_socket.send(bytes(msg,"utf-8"))


            

            #print("Message from Client_Address[",self.ipaddr,"]:",msg)

            client_socket.send(bytes("[Server]: Forwarded your message\n","utf-8"))
            

        print("Beende Client_Thread mit Addr\n",self.ipaddr)


def checkfor(port_addr,unions):

    port_addr = int(port_addr)

    for elements in unions:
        (union_socket,union_addr) = elements
        (union_ip,union_port) = union_addr
        print("Checkfor:",port_addr)
        print("Current:",union_port)
        if port_addr == union_port:
            return (union_socket,union_addr)
           
    
    return False


if __name__ == "__main__":
    
    print("Starte Main-Thread")

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',1337))
    server_socket.listen(2)

    all_clients = []
  

    while True:

        (client_socket,addr)= server_socket.accept()

        all_clients.append((client_socket,addr))

        ct = client_thread((client_socket,addr),all_clients)

        msg = "Deine Daten sind:" + str(addr)

        client_socket.send(bytes(msg,"utf-8"))

        ct.start()
        

    print("Beende Main-Thread")