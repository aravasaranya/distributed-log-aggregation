import socket
from datetime import datetime

HOST = "0.0.0.0"
PORTS = [10000, 10001]

sockets = []

for port in PORTS:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((HOST, port))
    sockets.append(s)

print("UDP Log Server started")
print("Normal logs: UDP 10000")
print("Critical logs: UDP 10001")

while True:
    readable, _, _ = __import__("select").select(sockets, [], [])

    for sock in readable:
        data, addr = sock.recvfrom(4096)
        received = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

        message = data.decode(errors="replace")

        print(f"[{received}] {addr[0]}:{addr[1]} -> {message}")

        ack = f"ACK|{message.split('|')[0]}"
        sock.sendto(ack.encode(), addr)
