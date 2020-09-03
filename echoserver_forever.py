import socketserver
from os.path import exists
import os
import codecs

HOST = ''
PORT = 9009

def FindFileinServerRepo(): # repo/server/ 아래의 파일과 디렉토리 출력
    ServerRepo = os.getcwd() + "/repo/server/"
    file_list = os.listdir(ServerRepo)
    sorted_file_list = []
    msg = "###디렉토리는 액세스 할 수 없습니다###\n"

    for file in file_list:
        if os.path.isfile(ServerRepo + file):
            sorted_file_list.append(("FILE", file))
        elif os.path.isdir(ServerRepo + file):
            sorted_file_list.append(("DIRECTORY", file))
    sorted_file_list.sort()

    for type, filename in sorted_file_list:
        if type == "FILE":
            msg += "[FILE] %s\n" % filename
        elif type == "DIRECTORY":
            msg += "[DIRECTORY] %s\n" % filename
    return msg



class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        self.service = self.request.recv(1024).decode() # 서비스 종류 받기

        # echo 서비스를 진행할 코드
        if self.service == "chat":
            print("채팅 시스템에 [%s] 연결됨!" %self.client_address[0])
            try:
                while True:
                    self.data = self.request.recv(1024)
                    if self.data.decode() == '/quit':
                        print("[%s] 사용자에 의해 중단" %self.client_address[0])
                        return
                    # /quit 메세지가 아닌 이상 계속해서 echo
                    print("[%s] %s" %(self.client_address[0], self.data.decode()))
                    self.request.sendall(self.data)

            except Exception as e:
                print(e)

        # 파일 송신 프로그램
        if self.service == "file_transfer":
            data_transferred = 0
            print("파일 전송 시스템에 [%s] 연결됨!" %self.client_address[0])

            filename = self.request.recv(1024).decode()

            server_file_path = os.getcwd() + "/repo/server/" + filename
            # print(server_file_path)

            if not exists(server_file_path):
                print("[%s] 존재하지 않음!" %server_file_path)
                return

            print("[%s] 전송 시작..." %filename)

            with open(server_file_path, 'rb') as file:
                try:
                    data = file.read(1024)  # file.read("byte") byte씩 읽는다. 넣지않을경우엔 한번에 다 읽는다.
                    while data:
                        data_transferred += self.request.send(data)
                        data = file.read(1024)

                except Exception as e:
                    print(e)

            print("전송 완료! [%d]Bytes" %data_transferred)

        if self.service == "file_upload":
            print("[%s]에서 파일 업로드" %self.client_address[0])
            server_file_path = os.getcwd() + "/repo/server/"
            filename = self.request.recv(1024).decode()

            data_transferred = 0
            with open(server_file_path + filename, 'wb') as file:
                try:
                    data = self.request.recv(1024)
                    while data:
                        file.write(data)
                        data_transferred += len(data)
                        data = self.request.recv(1024)
                except Exception as e:
                    print(e)

        if self.service == "file_list":
            print("[%s]에서 파일 탐색" %self.client_address[0])
            msg = FindFileinServerRepo()
            self.request.sendall(msg.encode())

def runServer():
    print("+++Echo/file transfer server is started")

    try: # TCP를 사용하며 HOST, PORT로 바인딩된 객체를 생성해 server로 둔다
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever() # Interrupt하기 전까지 계속 실행
    except KeyboardInterrupt:
        print("---Shutdown")

runServer()