import socket
import time

HOST = 'localhost'
PORT = 9009

def getFileFromServer(filename):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        service = "file_transfer"
        sock.sendall(service.encode())
        time.sleep(0.1) # waitting for server

        sock.sendall(filename.encode())
        data = sock.recv(1024) # 1024바이트씩 전달받아서 data에 모두 쌓는다
        data_transferred = 0
        if not data:
            print("no such file")
            return

        with open("repo/client/" + filename, 'wb') as file:
            try:
                while data:
                    file.write(data)
                    data_transferred += len(data)
                    data = sock.recv(1024)
            except Exception as e:
                print(e)

        print("[%s]의 전송완료. 크기 [%d]" %(filename, data_transferred))

while True:
    service = input("""무슨 서비스를 원하십니까?
'c': 채팅 시스템, 'f' 파일전송 : """)

    if service == 'c':
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            service = "chat"
            sock.send(service.encode()) # 서비스 종류를 알려줌

            while True:
                msg = input("Message: ")
                if msg == "/quit":
                    sock.sendall(msg.encode())
                    break

                sock.send(msg.encode())
                answer = sock.recv(1024)
                print("From server: %s" %answer.decode())
    elif service == 'f':
        filename1 = input("filename: ")
        getFileFromServer(filename1)
    else:
        print("c 또는 f를 입력하세요")