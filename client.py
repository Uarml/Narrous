import threading
import socket
import rsa
import colorama
from colorama import Fore, init

init(autoreset=True)

print(Fore.MAGENTA + "Narrous")
print("version, client aplpha 0.3")

public_key, private_key = rsa.newkeys(1024)
public_partner = None

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost", 33333))
client.send(public_key.save_pkcs1("PEM"))
public_partner = rsa.PublicKey.load_pkcs1(client.recv(1024))

stop = False


def send():
    while not stop:
        client.send(rsa.encrypt(input().encode('utf-8'), public_partner))


def rcv():
    while not stop:
        msg = rsa.decrypt(client.recv(1024), private_key).decode('utf-8')
        print((Fore.BLUE + "other dude: ") + (Fore.LIGHTYELLOW_EX + msg))


thread_1 = threading.Thread(target=send)
thread_2 = threading.Thread(target=rcv)

thread_1.start()
thread_2.start()
