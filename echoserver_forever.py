import socketserver

HOST = ''
PORT = 9009

class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("[%s] 연결됨!" %self.client_address[0])
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

def runServer():
    print("+++Echo server is started")
    try: # TCP를 사용하며 HOST, PORT로 바인딩된 객체를 생성해 server로 둔다
        server = socketserver.TCPServer((HOST, PORT), MyTcpHandler)
        server.serve_forever() # Interrupt하기 전까지 계속 실행
    except KeyboardInterrupt:
        print("---Shutdown")

runServer()