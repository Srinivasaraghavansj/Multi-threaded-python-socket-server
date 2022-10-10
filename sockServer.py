from concurrent.futures import thread
import socket               # Import socket module
import threading

__stop_request = False

def on_new_client(clientsocket: socket.socket, addr):
	try:
		while not __stop_request:
			msg = clientsocket.recv(1024).decode("utf-8")
			#do some checks and if msg == someWeirdSignal: break:
			print(addr, ' >> ', msg)
			msg = input('SERVER >> ')
			#Maybe some code to compute the last digit of PI, play game or anything else can go here and when you are done.
			clientsocket.send(msg.encode())
	finally:
		clientsocket.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = 'localhost'
port = 1099

print('Server started!')
print('Waiting for clients...')

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((host, port))
s.listen(5)

threads = []

try:
	while True:
		c, addr = s.accept()
		print('Got connection from', addr)
		threads.append(threading.Thread(target = on_new_client,kwargs = {'clientsocket': c.dup(),'addr': addr}))
		threads[-1].start()
		c.detach()
		#Note it's (addr,) not (addr) because second parameter is a tuple
		#Edit: (c,addr)
		#that's how you pass arguments to functions when creating new threads using thread module.
except KeyboardInterrupt:
	__stop_request = True
	for t in threads:
		t.join()
	s.close()
finally:
	__stop_request = True
	for t in threads:
		t.join()
	s.close()
