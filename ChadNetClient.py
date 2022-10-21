import socket
from tkinter import *
import time
import threading

HOST = "172.28.28.228"  # The server's hostname or IP address
PORT = 25565  # The port used by the server
FORMAT = "utf-8"
SIZE = 2048

window = Tk()
window.geometry("600x600")
window.title("ChadNet")
inputText = "Send message"


def login():
    title = Label(window, text="Log in:")
    usernameText = Label(window, text="Username")
    usernameEntry = Entry(window)
    passwordText = Label(window, text="Password")
    passwordEntry = Entry(window, show="*")
    loginButton = Button(window, text="Login", command=lambda: get_login(usernameText, usernameEntry, passwordText,
                                                                         passwordEntry, loginButton, signupButton,
                                                                         title, 0))
    signupButton = Button(window, text="Sign Up", command=lambda: get_login(usernameText, usernameEntry, passwordText,
                                                                            passwordEntry, loginButton, signupButton,
                                                                            title, 1))
    title.pack()
    usernameText.pack()
    usernameEntry.pack()
    passwordText.pack()
    passwordEntry.pack()
    loginButton.pack()
    signupButton.pack()


def send_message(entry, *args):
    message = entry.get()
    s.send(bytes(message, FORMAT))
    entry.delete(0, "end")


def get_login(usernameText, usernameEntry, passwordText, passwordEntry, loginButton, signupButton, title, signup, *args):
    if signup == 1:
        s.send(bytes("True", FORMAT))
    else:
        s.send(bytes("False", FORMAT))
    time.sleep(0.1)
    while True:
        name = usernameEntry.get()
        password = passwordEntry.get()
        s.send(bytes(name, FORMAT))
        time.sleep(0.1)
        s.send(bytes(password, FORMAT))
        usernameEntry.delete(0, "end")
        passwordEntry.delete(0, "end")
        data = s.recv(SIZE)
        title.destroy()
        usernameText.destroy()
        usernameEntry.destroy()
        passwordText.destroy()
        passwordEntry.destroy()
        loginButton.destroy()
        signupButton.destroy()
        if data.decode() == "Login successful":
            message()
            break
        elif data.decode() == "Try again":
            login()
            break
        else:
            break


def get_messages():
    while True:
        try:
            messageRecv = s.recv(SIZE).decode()
            if messageRecv != "":
                print(messageRecv)
                messageLabel = Label(window, text=messageRecv)
                messageLabel.pack()
                window.update()
        except:
            pass


def message():
    label = Label(window, text=inputText)
    entry = Entry(window)
    submit_button = Button(window, text="Send", command=lambda: send_message(entry))
    label.pack()
    entry.pack()
    submit_button.pack()
    threading.Thread(target=get_messages, daemon=True).start()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    login()
    window.mainloop()
