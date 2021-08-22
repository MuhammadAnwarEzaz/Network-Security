#!/usr/bin/env python
# coding: utf-8

# In[3]:


# This is Alice (client).

print('Welcome to STS, Alice!')

import sympy
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

key = open('AlicePrivateKey.pem', 'rb').read()
aliceprkey = RSA.importKey(key)

key = open('BobPublicKey.pem', 'rb').read()
bobpkey = RSA.importKey(key)

p = 0
while True:
    p = random.getrandbits(7)
    if sympy.isprime(p) and p>13:
        break
g = random.randint(2,p-1)
a = random.randint(1, p-1)
print("Generated Prime p =",p,"\nGenerated primitive element g =",g)
A = pow(g, a , p)
print("\nAlice's Private Number a =",a,"\nAlice's Public Number A =",A)
HOST = socket.gethostname()
PORT = 2987

client_socket = socket.socket()
print('Socket created')
print('Connecting to server...')
try:
    client_socket.connect((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()
    
print('Socket bind complete. Running authentication protocol...')

data = str(p) + '\n' + str(g) + '\n' + str(A)
client_socket.sendall(data.encode('ascii'))

data = client_socket.recv(4096).decode()
B = int(data)
client_socket.send("          ".encode())
Ekb = client_socket.recv(4096)
Kt = pow(B,a,p)
signatureB = decrypt(str(Kt), Ekb)
print("\nBob's Public Number B =",B,"\nAlice's Shared Secret K =",Kt,"\nEncrypted Message from Bob =",Ekb)
print("Decryted Message =",signatureB)

messageFromB = str(B) + str(A)
h = SHA512.new(messageFromB.encode('ascii'))
#print("Message Hashed at Alice's Side =",h)
verifier = PKCS1_v1_5.new(bobpkey)
if (verifier.verify(h, signatureB)):
    print("The signature received from the Bob is authentic.")
    print("Type 'exit' to quit this session.")
    
    message = str(A) + str(B)
    h = SHA512.new(message.encode('ascii'))
    signer = PKCS1_v1_5.new(aliceprkey)
    signatureA = signer.sign(h)
    Eka = encrypt(str(Kt), signatureA)
    print("\nConcatenated Message =",message,"\nSigned Message =",signatureA,"\nEncrypted Message =",Eka)
    client_socket.send(Eka)
    
    send = 0
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
            print("Waiting for Bob's message...");
            messageFromB = client_socket.recv(1024)
            XX = decrypt(str(Kt), messageFromB).decode()
            if (messageFromB == 'Authentication failed.'):
                print('Authentication failed.')
                XX = 'exit'
                
            if (XX != 'exit'):
                print('Bob said: ' + XX)
                send = 1
            else:
                print('Session terminated by Bob.')
                message = 'exit'

else:
    print("The signature received from the server is NOT authentic.")

client_socket.close()


# In[ ]:





# In[ ]:




