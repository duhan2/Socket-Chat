import socket
import threading

class client_thread(threading.Thread):

    username_list = {}

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

        client_socket.send(bytes("[Server]: Enter username\n","utf-8"))
        
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8")

        if (msg) not in client_thread.username_list.keys():

            client_thread.username_list[msg] = (self.client_socket,self.addr)

        username = msg

        while True:

            msg = "Current Userlist:\n" + str(client_thread.username_list)

            client_socket.send(bytes(msg,"utf-8"))

            
            msg = client_socket.recv(1024)
            msg = msg.decode("utf-8")

            #print("Eingegangene MEssage:",msg[0:i])

            checkforquit(msg,username,client_thread.username_list)    

            checkvalue = checkfor(msg,client_thread.username_list)

            if checkvalue == False:
                print("No User found\n")
                client_socket.send(bytes("No User found","utf-8"))
            else:
                (destclient_socket,destclient_addr) = checkvalue
                destclient_socket.send(bytes(msg,"utf-8"))


            

            #print("Message from Client_Address[",self.ipaddr,"]:",msg)

            client_socket.send(bytes("[Server]: Forwarded your message\n","utf-8"))
            

        print("Beende Client_Thread mit Addr\n",self.ipaddr)


def checkfor(msg,username_list):

    i = 0

    for c in msg:

        if c == ':':
            
            break

        i = i+1

    username = msg[0:i]

    for entries in username_list.keys():
        
        #print("Checkfor:",username)
        #print("Current:",entries)
        if username == entries:
            return username_list[entries]
           
    
    return False

def checkforquit(msg,username,username_list):

    if msg == "Server:quit":
        for entries in username_list.keys():
            if username == entries:
                username_list[entries] = "User disconnected"

    
        


if __name__ == "__main__":
    
    print("Starte Main-Thread")

    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',1337))
    server_socket.listen(2)

    while True:

        (client_socket,addr)= server_socket.accept()

        
        ct = client_thread((client_socket,addr))

        #msg = "Deine Daten sind:" + str(addr)

        #client_socket.send(bytes(msg,"utf-8"))

        ct.start()
        

    print("Beende Main-Thread")