import socket
import threading

class client_thread(threading.Thread):

    username_list = {} #Variable über Konstruktor damit jeder Clientthread darauf zugreifen kann

    def __init__(self,union):
       
        threading.Thread.__init__(self) #Standard für Threads

        #Aufteilen des Tupels in kleinere Variablen
        (client_socket,addr) = union 
        (ipaddr,portno) = addr

        print("Client verbunden mit IP-Adresse:",ipaddr," und Portnummer:",portno,"\n")

        #Variablen zuweisen um die in anderen Methoden aufrufen zu können
        self.client_socket = client_socket
        self.addr = addr
        self.ipaddr = ipaddr
        self.portno = portno
    
    def run(self):

        #Nachrichten werden kodiert versendet mit bytes() und decodiert mit decode()
        client_socket.send(bytes("[Server]: Enter username\n","utf-8"))
        
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8")

        #Falls User noch nicht in Liste, dann anlegen
        if (msg) not in client_thread.username_list.keys():
            client_thread.username_list[msg] = (self.client_socket,self.addr)

        username = msg

        while True:

            #Wiederholtes sender der aktuellen Userlist
            msg = "Current Userlist:\n" + str(client_thread.username_list)
            client_socket.send(bytes(msg,"utf-8"))

            #Wiederholtes Empfangen der Nachricht
            msg = client_socket.recv(1024)
            msg = msg.decode("utf-8")

            #Überprüfen ob Client disconnecten will
            checkforquit(msg,username,client_thread.username_list)    
            #Überprüfen ob Nachricht an User gerichtet ist
            checkvalue = checkfor(msg,client_thread.username_list)

            if checkvalue == False:
                print("No User found\n")
                client_socket.send(bytes("No User found","utf-8"))
            else:
                (destclient_socket,destclient_addr) = checkvalue #Nachricht an Tupel weiterleiten
                destclient_socket.send(bytes(msg,"utf-8"))


            #client_socket.send(bytes("[Server]: Forwarded your message\n","utf-8"))
            
        #print("Beende Client_Thread mit Addr\n",self.ipaddr)


def checkfor(msg,username_list):
    #Geht Nachricht bis zum ":" durch
    i = 0

    for c in msg:

        if c == ':':
            
            break

        i = i+1

    username = msg[0:i]

    #Gucken ob User existiert, wenn ja gib Tupel zurück
    for entries in username_list.keys():
        
        if username == entries:
            return username_list[entries]
           
    
    return False

def checkforquit(msg,username,username_list):
    #Überprüfen ob der Client disconnecten wird
    if msg == "Server:quit":    #wenn ja wird sein Eintrag überschrieben 
        for entries in username_list.keys():
            if username == entries:
                username_list[entries] = "User disconnected"

    
        


if __name__ == "__main__":
    
    print("Starte Main-Thread")

    #Initialize und bind Socket. Dann 
    server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1',1337))
    server_socket.listen(2) #Anzahl der abhörbaren Sockets

    while True:
        #Tupel was accept() zurückgibt
        (client_socket,addr)= server_socket.accept()
        #Jeder Client kriegt eine Threadklassenvariable
        ct = client_thread((client_socket,addr))
        #Diese Methode startet die run() Methode
        ct.start()
        

    print("Beende Main-Thread")