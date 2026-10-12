import socket
import sys
import time

SERVER = sys.argv[1] if len(sys.argv) > 1 else "10.0.0.4"
SEVERITY = sys.argv[2] if len(sys.argv) > 2 else "NORMAL"

PORT = 10001 if SEVERITY == "CRITICAL" else 10000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2)

for seq in range(1, 11):
    timestamp = time.time()
    message = f"{seq}|{SEVERITY}|{timestamp}|Application log from client"

    start = time.time()
    sock.sendto(message.encode(), (SERVER, PORT))

    try:
        data, _ = sock.recvfrom(4096)
        delay = (time.time() - start) * 1000
        print(f"Sent {seq} | {SEVERITY} | ACK received | {delay:.2f} ms")
    except socket.timeout:
        print(f"Sent {seq} | {SEVERITY} | PACKET LOST")

    time.sleep(0.2)

sock.close()
