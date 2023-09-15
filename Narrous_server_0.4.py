import socket
import threading
import rsa
import colorama
from colorama import Fore, init

# resetting the color after printing
init(autoreset=True)

# printing Narrous
print(Fore.MAGENTA + "Narrous")
print("version, server aplpha 0.4")

#connecting to the server and generating keys
public_partner = None
public_key, private_key = rsa.newkeys(1024)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 33300))
server.listen()

client, addr = server.accept()
client.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

disabled = False

# encoding, encrypting and sending
def send():
    while not disabled:
        client.send(rsa.encrypt(input().encode('utf-8'), public_partner))

def recv():
    while not disabled:
        msg = rsa.decrypt(client.recv(1024), private_key).decode('utf-8')
        print((Fore.BLUE + "other dude: ") + (Fore.LIGHTGREEN_EX + msg))

# starting threads
thread_1 = threading.Thread(target=recv)
thread_2 = threading.Thread(target=send)

thread_1.start()
thread_2.start()
