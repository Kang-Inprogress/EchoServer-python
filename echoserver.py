# 1회성 서버
import socket

HOST = ''
PORT = 9009
def runServer():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((HOST, PORT))
        sock.listen(1)
        print("Waitting for users...")

        connected_socket, addr = sock.accept()
        with connected_socket:
            print("클라이언트 연결됨: %s" % addr[0])
            while True:
                data = connected_socket.recv(1024) # 1024~4096
                if not data:
                    break
                print("보내어진 메세지: %s" %data.decode())
                connected_socket.sendall(data)

runServer()