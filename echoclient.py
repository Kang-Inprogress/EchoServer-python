import socket

HOST = 'localhost'
PORT = 9009

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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))
            service = "file_transfer"
            sock.send(service.encode()) # 서비스 종류를 알려줌

            data_transfer = 0   # 서버로 부터 받아온 파일 크기

            filename = input("받을 파일의 이름: ")    # 나중에 함수로 다시 쓸때는 파라미터로 가지고 올 것
            sock.send(filename.encode())

            data = sock.recv(1024)
            if not data:
                print("파일 [%s]: 서버에 존재하지 않거나 전송중 오류발생" %filename)
                # return

            with open("repo/client/" + filename, 'wb') as file:
                try:
                    while data:
                        file.write(data)
                        data_transfer += len(data)
                        data = sock.recv(1024)
                except Exception as e:
                    print(e)

            print("파일 [%s] 전송완료. 전송량 [%d] Bytes" %(filename, data_transfer))

    else:
        print("c 또는 f를 입력하세요")