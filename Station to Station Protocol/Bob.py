#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This is Bob (server).

print('Welcome to STS, Bob!')

import sys
import math
import socket
import random
import hashlib
from Crypto.Hash import SHA512
from Crypto.Random import random
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from simplecrypt import encrypt, decrypt

key = open('BobPrivateKey.pem', 'rb').read()
bobprkey = RSA.importKey(key)

key = open('AlicePublicKey.pem', 'rb').read()
alicepkey = RSA.importKey(key)

HOST = socket.gethostname()
PORT = 2987 

server_socket = socket.socket()
print('Socket created')

try:
    server_socket.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()

print('Socket bind complete')
server_socket.listen(5)
print('Socket now listening')

(client_socket, address) = server_socket.accept()    
print('Got connection from client ' + address[0] + '. Running authentication protocol...')

data = client_socket.recv(4096).decode()
#print(data)
temp = data.split('\n')
p = int(temp[0])
g = int(temp[1])
A = int(temp[2])
b = random.randint(1, p-1)
B = pow(g, b, p)
Kt = pow(A, b, p)
print("\nGenerated Prime =",p,"\nGenerated Primitive Element =",g,"\nAlice's Public Number =",A)
print("\nBob's Private Number b =",b,"\nBob's Public Number B =",B,"\nBob's Shared Secret K =",Kt)

message = str(B) + str(A)
XX = message.encode('ascii')
#print(XX)
h = SHA512.new(message.encode('ascii'))
signer = PKCS1_v1_5.new(bobprkey)
signatureB = signer.sign(h)
Ekb = encrypt(str(Kt), signatureB)
data = str(B)
data1 = Ekb
print("\nConcatenated Message =",message,"\nSigned Message =",signatureB,"\nEncrypted Message =",Ekb)
client_socket.send(data.encode('ascii'))
client_socket.recv(4096)
client_socket.send(data1)

Eka = client_socket.recv(1024)
if (Eka != ''):
    signatureA = decrypt(str(Kt), Eka)
    print("Decryted Message =",signatureA)
    messageFromA = str(A) + str(B)
    h = SHA512.new(messageFromA.encode('ascii'))
    verifier = PKCS1_v1_5.new(alicepkey)
    if (verifier.verify(h, signatureA)):
        print("The signature received from the client is authentic.")
        print("Type 'exit' to quit this session.")
        
        send = 1
        while(message != 'exit'):
            if (send == 1):
                message = input('Your message: ')
                if (message == 'exit'):
                    print('Session terminated.')
                    client_socket.send(message.encode())
                else:
                    encrypted = encrypt(str(Kt), message)
                    client_socket.send(encrypted)
                    print('Message sent successfully.');
                    send = 0
            elif (send == 0):
                print("Waiting for Alice's message...")
                messageFromA = client_socket.recv(1024)
                XX = decrypt(str(Kt), messageFromA).decode()
                if (XX != 'exit'):
                    print('Alice said: ' + XX)
                    send = 1
                else:
                    print('Session terminated by Alice.')
                    message = 'exit'
            
    else:
        print("The signature received from the client is NOT authentic.")
        client_socket.send("Authentication failed.")
else:
    print("Authentication failed.")

client_socket.close()
server_socket.close()


# In[ ]:





# In[ ]:




