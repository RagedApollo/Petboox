import socket
from queue import Queue, Empty
from threading import Thread
import select


HOST = "172.28.28.228"
PORT = 25565
SIZE = 2048
FORMAT = "utf-8"


def newClient(conn, ip, q):
    ipAdress, port = ip
    with conn:
        print("Connected with: " + ipAdress)
        while True:
            signup = conn.recv(SIZE).decode()
            name = conn.recv(SIZE).decode()
            password = conn.recv(SIZE).decode()
            if signup == "True":
                login = open("Login.txt")
                if name not in login.read():
                    login.close()
                    login = open("Login.txt", "a")
                    login.write(name + ' : ' + password + " + " + ipAdress + "\n")
                    conn.sendall(bytes("Login successful", FORMAT))
                    print("Sign Up successful")
                    login.close()
                    break
                else:
                    print("Name already in use")
                    conn.sendall(bytes("Try again", FORMAT))
            else:
                login = open("Login.txt", 'r')
                if name in login.read():
                    login.seek(0)
                    for line in login.readlines():
                        if name in line:
                            if password in line:
                                print("Login successful")
                                conn.sendall(bytes("Login successful", FORMAT))
                                break
                            else:
                                print("Wrong password")
                                conn.sendall(bytes("Try again", FORMAT))
                    else:
                        print("Not good")
                        conn.sendall(bytes("Try again", FORMAT))
                        continue
                    break
                else:
                    print("User not found")
                    conn.sendall(bytes("Try again", FORMAT))
        login.close()
        person = name
        print(f"\nConnected by {person}\n")
        while True:
            try:
                s.setblocking(True)
                ready = select.select([conn], [], [], 1)
                if ready[0]:
                    data = conn.recv(SIZE)
                    text = data.decode()
                    if not data:
                        print(f"\n{person} disconnected\n")
                        break
                    if text != "":
                        message = f"{person}: " + text
                        print(message)
                        q.put(message)
            except:
                print(f"\n{person} disconnected\n")
                break
            try:
                message = q.get(False)
                if f"<{person}>" in message:
                    message = message.replace(f"<{person}>", "")
                    conn.send(bytes(message, FORMAT))
                    print(message)
                else:
                    q.put(message)
            except Empty:
                pass
            except Exception:
                print(Exception)
            else:
                pass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    q = Queue()
    s.bind((HOST, PORT))
    s.listen(5)
    while True:
        conn, ip = s.accept()
        Thread(target=newClient, args=(conn, ip, q),daemon=True).start()
