import socket, time, ast

def output(chunk) :
	chunk = ast.literal_eval(chunk)
	
	if (chunk[1] == '366') :
		return ('You', 'You can now send messages')

	if chunk[0] == 'PING' :
		return ('Server', 'ponged')

	username = chunk[0].split(':')[1].split('!')[0]
	index = chunk.index("#bots") + 1
	container = chunk[index:]
	message = " ".join(word for word in container)
	message = message[1:]
	return (username, message)

echo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True :
	try:
		print("Conecting to ('0.0.0.0', 1717)")
		name = x = socket.gethostname()
		echo.connect((name, 1717))
		print('Conn. Successful')
		break
	except Exception as e :
		print('Connection Unsucessful because:\n{}'.format(e))
		print('Attempting to reconnect in 5 seconds')
		time.sleep(5)

while True :
	try :
		irc = echo.recv(1024).decode()
		if not irc :
			continue
		message = output(irc)
		print('[{0}] :>>> {1}'.format(message[0], message[1]))
	except Exception as e :
		print(e)
		echo.close()
		print('Closing in 10 seconds')
		time.sleep(10)
		break


