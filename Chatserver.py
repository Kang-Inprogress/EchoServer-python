import socketserver
import threading

HOST = ''
PORT = 9009
lock = threading.Lock()

class UserManager:
    def __init__(self): # 클래스 생성시 호출
        self.users = {} # 공용 데이터로써 Threading lock을 사용해야한다

    def addUser(self, username, connected_socket, addr):
        if username in self.users:
            connected_socket.send("이미 등록된 사용자 입니다.\n".encode())
            return None
        # 새로운 사용자 등록
        lock.acquire()
        self.users[username] = (connected_socket, addr)
        lock.release()

        self.sendMessageToAll("[%s]님이 입장했습니다." %username)
        print("+++ 대화 참여자 수 [%d]" %len(self.users))

        return username

    def removeUser(self, username):
        if username not in self.users:
            return

        lock.acquire()
        del self.users[username]
        lock.release()

        self.sendMessageToAll("[%s]님이 퇴장햇습니다." %username)
        print("--- 대화 참여자 수 [%d]" %len(self.users))

    def messageHandler(self, username, msg):
        if msg[0] != '/':
            self.sendMessageToAll("[%s] %s" %(username, msg))
            return
        else:
            if msg.strip() == "/quit":
                self.removeUser(username)
                return -1

    def sendMessageToAll(self, msg):
        for conn, addr in self.users.values():
            conn.send(msg.encode())


class MyTcpHandler(socketserver.BaseRequestHandler):
    usermanager = UserManager()

    def handle(self):
        print("[%s] 연결됨" %self.client_address[0])

        try:
            username = self.registerUsername()
            msg = self.request.recv(1024)
            while msg:
                print("[%s:%s] %s" %(self.client_address[0],username, msg.decode()))
                if self.usermanager.messageHandler(username, msg.decode()) == -1:
                    self.request.close()
                    break
                msg = self.request.recv(1024)
        except Exception as e:
            print(e)
        print("[%s] 접속 종료" %self.client_address[0])
        self.usermanager.removeUser(username)

    def registerUsername(self):
        while True:
            self.request.send("로그인 ID:".encode())   # self.request는 소켓이다..
            username = self.request.recv(1024)
            username = username.decode().strip()
            if self.usermanager.addUser(username, self.request, self.client_address):
                return username

class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
    print("+++ 채팅 서버를 시작합니다.")

    try:
        server = ChatingServer((HOST, PORT), MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("--- 채팅 서버를 종료합니다.")
        server.shutdown()
        server.server_close()

runServer()