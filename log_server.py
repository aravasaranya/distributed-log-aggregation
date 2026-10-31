import socket
import json
import select
from pathlib import Path
from datetime import datetime

HOST = "0.0.0.0"
PORTS = [10000, 10001]
LOG_FILE = Path(__file__).resolve().parent / "d2_dashboard" / "logs.jsonl"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

sockets = []

for port in PORTS:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port))
    sockets.append(sock)

print("UDP Log Server started")
print("Normal logs: UDP 10000")
print("Critical logs: UDP 10001")
print(f"Dashboard log file: {LOG_FILE}")

while True:
    readable, _, _ = select.select(sockets, [], [])

    for sock in readable:
        data, addr = sock.recvfrom(4096)
        received = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        message = data.decode(errors="replace")

        print(f"[{received}] {addr[0]}:{addr[1]} -> {message}")

        parts = message.split("|", 3)
        severity = "CRITICAL" if sock.getsockname()[1] == 10001 else "NORMAL"

        record = {
            "timestamp": received,
            "host": addr[0],
            "severity": severity,
            "message": message
        }

        with LOG_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")

        ack = f"ACK|{message.split('|')[0]}"
        sock.sendto(ack.encode(), addr)
