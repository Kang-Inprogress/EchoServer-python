import socket
import time
from os.path import exists
import os
import codecs

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

def getFileListFromServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        service = "file_list"
        sock.sendall(service.encode())

        servermsg = sock.recv(1024).decode()
        print(servermsg)

def putFile():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        service = "file_upload"
        sock.sendall(service.encode())

        repo_path = os.getcwd() + "/repo/client/"
        data_transferred = 0
        while True:
            filename = input("업로드 할 파일명: ")
            if not exists(repo_path + filename):
                print("not exists")
                break
            else:
                sock.send(filename.encode()) # 저장될 파일 이름 전송
                with open(repo_path + filename, 'rb') as file:
                    try:
                        data = file.read(1024)
                        while data:
                            sock.send(data)
                            data_transferred += len(data)
                            data = file.read(1024)
                    except Exception as e:
                        print(e)
                print("업로드 완료")

# Main
while True:
    service = input("""무슨 서비스를 원하십니까?
'c': 채팅 시스템  'f' 파일 다운로드  'u' 파일 업로드  'l' 저장소탐색  '/quit' 나가기 : """)

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
    elif service == 'u':
        putFile()
    elif service == 'l':
        getFileListFromServer()
    elif service == "/quit":
        break
    else:
        print("c 또는 f를 입력하세요")