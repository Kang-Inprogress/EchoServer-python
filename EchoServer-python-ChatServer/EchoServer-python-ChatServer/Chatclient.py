import socket
from threading import Thread

HOST = "localhost"
PORT = 9010

def rcvMsg(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print(data.decode())
        except:
            pass

def runChat():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        # print("연결됨")
        t = Thread(target=rcvMsg, args=(sock,)) # rcvMsg함수를 독립적으로 실행 가능한 스레드로 만들어준다
        t.daemon = True # t를 생성한 메인 스레드(runChat())가 종료하면 자동적으로 종료하게 해준다
        t.start()
        # print("스레드 생성됨")

        while True:
            msg = input("대화: ")
            if msg == "/quit":
                sock.send(msg.encode())
                break
            sock.send(msg.encode())

runChat()