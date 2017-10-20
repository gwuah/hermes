import sys
import socket
import threading
from datetime import datetime


global port_in_use


NICK = "griffmaestro"
INDENT = "griffmaestro"
REALNAME = "gwuahnode"
MASTER = "gwuahnode"
channel = "#bots"

port_in_use = True

_address = ("irc.freenode.net", 6667)
out_add = ('', 1717)
_buffer = ''


irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
echo = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
	echo.bind(out_add)
	echo.listen(1)
	print('ECHO ACTIVE')
	sockfd, addr = echo.accept()
except Exception as e :
	print(e)

def connect(_address) :
	irc.connect(_address)
	return True

def reg_userinfo():
	irc.send(bytes("NICK %s\r\n" % NICK, "UTF-8"))
	irc.send(bytes("USER %s %s rat :%s\r\n" % (INDENT, _address[0], REALNAME), "UTF-8"))
	irc.send(bytes("JOIN %s\r\n" % channel, "UTF-8"))
	irc.send(bytes("PRIVMSG %s :ogma \r\n" % MASTER, "UTF-8"))
	return True


def recv() :
	message = _buffer + irc.recv(1024).decode("UTF-8")
	return message


def irc_center() :
	while 1 :
		_buffer = recv()
		if not _buffer :
			continue
		message = _buffer.split("\n")
		_buffer = message.pop()

		for line in message :
			line = line.rstrip()
			line = line.split()

			if len(line) <= 1 :
				pass
			
			if len(line) >= 2 :
				if (line[1] == '366') :
					sockfd.send(str(line).encode())
					
				if (line[0] == "PING") :
					irc.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
					sockfd.send(str(line).encode())

				if (line[1] == "PRIVMSG") :
					sockfd.send(str(line).encode())

def main() :
	center = threading.Thread(target=irc_center)

	if connect(_address) :
		print('Connected to GWUAH-SERVER')
		print("You're Welcome\n")
		if reg_userinfo():
			print('Registering your client.')
			print('Registered on Network')

			center.start()

			while True :
				msg = input('[You] :>>> ')
				irc.send(bytes("PRIVMSG "+ "#bots" +" :"+ msg +"\n", "UTF-8"))

main()