import socket
import threading
import sqlite3
import rsa
from datetime import datetime


class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        print("[+] New thread for %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connexion from %s %s" % (self.ip, self.port,))



        code = self.clientsocket.recv(2048)
        mess = code.decode("utf-8")
        mess = mess[2::]
        #we define two mods : 1 is for login, 2 is for datasending
        #
        #
        #  % IS FOR DATA, ^ IS FOR ACTION ID ( AKA LOG,REG,SEND )
        #
        #
        actionId = mess.split("^")[0]
        #autor gives us or not the authorization to send confirmation of good log/reg to user
        autor = 0
        data = mess.split("^")[1]
        print(data)
        if actionId == "1" :
            #REGISTER
            print("registering")
            autor = self.sqlFuncRegister(data)
            self.sendAutor(autor)
        elif actionId == "2" :
            #LOGIN
            print("loging")
            autor = self.sqlFuncLogin(data)
            self.sendAutor(autor)
        elif actionId == "3" :
            print("ON EST LA")
            autor = self.sqlDATA(data)
            print(autor)
            self.sendAutor(autor)

        else :
            print("BADABOUM, we're HACKED")


    def sendAutor(self,autor):
        if autor == 1 :
            #Good log/reg
            print("good log")
            message_to_send = "1^good account".encode("UTF-8")
            clientsocket.send(len(message_to_send).to_bytes(2, byteorder='big'))
            clientsocket.send(message_to_send)

        elif autor == 0 :
            #Bad log/reg
            print("bad log")
            message_to_send = "0^Bad log/reg".encode("UTF-8")
            clientsocket.send(len(message_to_send).to_bytes(2, byteorder='big'))
            clientsocket.send(message_to_send)

        elif autor == 2 :
            print("error")
            message_to_send = "Error".encode("UTF-8")
            clientsocket.send(len(message_to_send).to_bytes(2, byteorder='big'))
            clientsocket.send(message_to_send)
            return ("error")

        elif autor == 3 :
            print("2*day")
            message_to_send = "Not two times in a day !".encode("UTF-8")
            clientsocket.send(len(message_to_send).to_bytes(2, byteorder='big'))
            clientsocket.send(message_to_send)
            return("Salut bye bye")

        elif autor == 4 :
            print("S&R")
            message_to_send = "Sent and received !".encode("UTF-8")
            clientsocket.send(len(message_to_send).to_bytes(2, byteorder='big'))
            clientsocket.send(message_to_send)
            return("okk")



    def sqlDATA(self,data):
        data1 = data.split("%")[0]  # id
        now = datetime.now()  # current date and time
        date_time = now.strftime("%d/%m/%Y")
        mess = data.split("%")[1]  # mess
        print(mess)
        fichierDonnees = "/home/nicolas/Bureau/SQL_SERV/bd_login.sq3"
        conn = sqlite3.connect(fichierDonnees)
        cur = conn.cursor()

        fichierDonnees1 = "/home/nicolas/Bureau/SQL_SERV/bd_data.sq3"
        conn1 = sqlite3.connect(fichierDonnees1)
        cur1 = conn1.cursor()
        cur1.execute(
            "CREATE TABLE IF NOT EXISTS QUIZZ_DATA (ID TEXT, DAY_DATE DATE, ANSWERS TEXT)")

        cur.execute(
            "CREATE TABLE IF NOT EXISTS PATIENTS (ID TEXT, PASSWORD TEXT, YEAR_BIRTH YEAR , F_DATE1 DATE, F_DATE2 DATE, F_DATE3 DATE, PCOS_DETEC INT)")

        a = 0
        cur.execute("SELECT * FROM PATIENTS")
        for l in cur:
            if l[0] == data1:
                # the user logs in
                a = 2

        cur1.execute("SELECT * FROM QUIZZ_DATA")
        print(type(data1),type(date_time))
        for l in cur1:
            print(type(l[0]),type(l[1]))
            if (l[0],l[1]) == (data1,date_time):
                # the user as already sent data todday
                print("NEIN NEIN NEIN")
                a = 3
        if a == 0 or a == 3 :
            if a == 0 :
                a = 2
            print("MY GOD")
            return a
        conn.commit()
        cur.close()
        conn.close()
        print("SAVING DATA")


        data = (data1, date_time, mess)

        # registered in the database
        cur1.execute("INSERT INTO QUIZZ_DATA VALUES ( ?,?,?)", data)
        conn1.commit()
        cur1.close()
        conn1.close()
        return 4

    def sqlFuncLogin(self,data):

        fichierDonnees = "/home/nicolas/Bureau/SQL_SERV/bd_login.sq3"
        conn = sqlite3.connect(fichierDonnees)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS PATIENTS (ID TEXT, PASSWORD TEXT, YEAR_BIRTH YEAR , F_DATE1 DATE, F_DATE2 DATE, F_DATE3 DATE, PCOS_DETEC INT)")

        data1 = data.split("%")[0]  # id, on vérifie que l'id n'est pas déja dedans
        data2 = data.split("%")[1]

        cur.execute("SELECT * FROM PATIENTS")
        for l in cur:
            if (l[0],l[1]) == (data1,data2):
                # the user logs in
                conn.commit()
                cur.close()
                conn.close()
                return 1
        conn.commit()
        cur.close()
        conn.close()

        return 0


    def sqlFuncRegister(self,data):

        fichierDonnees = "/home/nicolas/Bureau/SQL_SERV/bd_login.sq3"
        conn = sqlite3.connect(fichierDonnees)
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE IF NOT EXISTS PATIENTS (ID TEXT, PASSWORD TEXT, YEAR_BIRTH YEAR , F_DATE1 DATE, F_DATE2 DATE, F_DATE3 DATE, PCOS_DETEC INT)")

        data1 = data.split("%")[0]  # id, on vérifie que l'id n'est pas déja dedans
        data2 = data.split("%")[1]  # password
        data3 = data.split("%")[2]  #Y Birth
        data4 = data.split("%")[3]  #Date1
        data5 = data.split("%")[4]  #Date2
        data6 = data.split("%")[5]  #Date3
        data7 = data.split("%")[6]  #Pcos confirmed

        data = (data1,data2,data3,data4,data5,data6,data7)

        cur.execute("SELECT * FROM PATIENTS")
        for l in cur:
            if l[0] == data1:
                if l[1] == data2 :
                    #ALREADY IN THE DATABASE
                    cur.close()
                    conn.close()
                    return 1
                #ID in the database, bad password
                cur.close()
                conn.close()
                return 0

        #registered in the database
        cur.execute("INSERT INTO PATIENTS VALUES ( ?,?,?,?,?,?,?)",data)
        conn.commit()
        cur.close()
        conn.close()
        return 1




#Server running
tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#3456 cause it's life
tcpsock.bind(("", 3456))
while True:
    tcpsock.listen(10)
    print("Listening...")

    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()



