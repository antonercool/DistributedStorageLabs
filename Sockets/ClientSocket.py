from os import read

from socket import *
import readchar

def get_status():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("localhost", 9000))
    s.send(bytes('GET status', 'utf-8'))
    data = s.recv(10000)
    print(data)
    s.close()
    
if __name__ == '__main__': 
    

    exit = 0
    while exit == 0:
        c = readchar.readchar()
        if c == b'\x18':
            exit = -1
        elif c == b'\r':
            print("pressed enter")
            get_status()

    