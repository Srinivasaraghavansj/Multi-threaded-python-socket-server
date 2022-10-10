import socket
import time
import random

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1099  # The port used by the server

id = random.randint(0, 100)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	s.connect((HOST, PORT))
	time.sleep(1)
	while True:
		msg = f"Hello, world{id}"
		s.sendall(msg.encode())
		print(f"Sent Hello, world {id}")
		data = s.recv(1024)
		print(f"Received {data!r}")
finally:
    s.close()
