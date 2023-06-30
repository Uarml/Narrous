import socket
import threading
import rsa
import colorama
from colorama import Fore, init

init(autoreset=True)

print(Fore.MAGENTA + "Narrous")
print("version, server aplpha 0.3")

public_key, private_key = rsa.newkeys(1024)
public_partner = None

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 33333))
server.listen()

client, addr = server.accept()
client.send(public_key.save_pkcs1("PEM"))

public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

stop = False


def recv():
    while not stop:
        msg = rsa.decrypt(client.recv(1024), private_key).decode('utf-8')
        print((Fore.BLUE + "other dude: ") + (Fore.LIGHTGREEN_EX + msg))


def send():
    while not stop:
        client.send(rsa.encrypt(input().encode('utf-8'), public_partner))


thread_1 = threading.Thread(target=recv)
thread_2 = threading.Thread(target=send)

thread_1.start()
thread_2.start()
