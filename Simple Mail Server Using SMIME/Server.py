#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
import socket

print("THIS IS SERVER\n")
HOST = socket.gethostname()
PORT1 = 2345
PORT2 = 2346

socket1 = socket.socket()
socket2 = socket.socket()
print('Sockets created')
print('Connecting to clients')

try:
    socket1.bind((HOST, PORT1))
    socket2.bind((HOST, PORT2))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()
    
print('Socket bind complete')
socket1.listen(5)
socket2.listen(5)
print('Socket now listening')

(socket1, address1) = socket1.accept() 
print('Got connection from client ' + address1[0])
(socket2, address2) = socket2.accept() 
print('Got connection from client ' + address2[0])

UserPassword = {'Alice':'alice','Bob':'bob'}
Users = {'alice@localhost':socket1,'bob@localhost':socket2}
userpw = socket1.recv(1024)
userpw = userpw.split(b'\n')
s1 = s2 = 0
if userpw[0].decode() in UserPassword:
    if userpw[1].decode() == UserPassword[userpw[0].decode()]:
        socket1.send('Authorised'.encode())
        s1 = 1
    else:
        socket1.send('Password Incorrect'.encode())
else:
    socket1.send('Username Incorrect'.encode())

userpw = socket2.recv(1024)
userpw = userpw.split(b'\n')
if userpw[0].decode() in UserPassword:
    if userpw[1].decode() == UserPassword[userpw[0].decode()]:
        socket2.send('Authorised'.encode())
        s2 = 1
    else:
        socket2.send('Password Incorrect'.encode())
else:
    socket2.send('Username Incorrect'.encode())

msg = ''
message = []
if s1 != 0:
    msg = socket1.recv(10000000)
    message = msg.split(b'\n\n\n\n\n')
    print('Message Coming from:',message[0])
    print('Message Going to:', message[1])
    socket1.send('You can exit'.encode())
else:
    print('Sender authentication failed')
#print(message[0],message[1])
if s2 != 0:
    if msg != ' ':
        socket2.send(msg)
        print('Message redirected to:',message[1])
    else:
        socket2.send('No Message for you (you can exit)')
else:
    print('Reciever authentication failed')

socket1.close()
socket2.close()


# In[ ]:




