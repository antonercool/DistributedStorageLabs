from socket import *

if __name__ == '__main__': 

    s = socket(AF_INET, SOCK_STREAM)
    s.bind(("", 9000))
    s.listen(5)
    while True:
        c,a = s.accept()
        data = c.recv(10)
        print(data)
        if data == b"GET status":    
            print("Status req rechived")
            c.send(bytes(f"Hello {a[0]}, Status is good", "utf-8"))
        c.close()

   
    