import socket

HOST = '192.168.111.100'
PORT = 9009

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    while True:
        msg = input("Message: ")
        if msg == "/quit":
            sock.sendall(msg.encode())
            break

        sock.send(msg.encode())
        answer = sock.recv(1024)
        print("From server: %s" %answer.decode())

