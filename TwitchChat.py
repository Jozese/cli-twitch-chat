import socket
import sys
import json
import threading
import time
from MessageParser import Parser


class TwitchChat(threading.Thread):
    def __init__(self) -> None:
        super().__init__()
        self.ttv_hostname = ""
        self.ttv_port = ""
        self.ttv_oauth = ""
        self.ttv_username = ""
        self.ttv_channel = ""
        
        self.parser = Parser()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_connection()

    def sock_connection(self) -> None:
        self.get_attributes()
        try:
            self.sock.connect((self.ttv_hostname,self.ttv_port))
            self.ttv_auth()
        except socket.error:
            print("Could not connect to remote server! ")
    
    def get_attributes(self) -> None:
        with open("settings.json","r") as f:
            data = json.load(f)
        self.ttv_hostname = data["hostname"]
        self.ttv_port = data["port"]
        self.ttv_oauth = data["token"]
        self.ttv_username = data["username"]
        self.ttv_channel = data["channel"]
    
    def ttv_auth(self) -> None:
        messages = [f"PASS oauth:{self.ttv_oauth}\n".encode(),f"NICK {self.ttv_username}\n".encode(),f"JOIN #{self.ttv_channel}\n".encode(),"CAP REQ :twitch.tv/tags\n".encode()]

        for message in messages:
            self.sock.sendall(message)
        data = self.sock.recv(4096).decode()
        if "GLHF!" in data:
            print("Connected to twitch's irc server!")
        else:
            print("Could not connect to twitch's irc server: Wrong auth/username")
        

    
    def recv_message(self) -> None:
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                message = self.parser.parse(data)
                if "PRIVMSG" in data:
                    print(message)
            except Exception as e:
                pass
            

    def run(self) -> None:
        self.recv_message()


        
tw = TwitchChat()
tw.start()

while True:
    time.sleep(100)

        