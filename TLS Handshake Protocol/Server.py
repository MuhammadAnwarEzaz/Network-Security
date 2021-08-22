#!/usr/bin/env python
# coding: utf-8

# In[10]:


import sympy
import socket
import random
from Crypto.Hash import SHA,MD5,HMAC
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import codecs
import numpy as np

def PRF(secret,seed):
    a0 = seed
    secret1 = secret[:512]
    secret2 = secret[512:]
    a1 = HMAC.new(secret1, msg=a0, digestmod=SHA).digest()
    a2 = HMAC.new(secret1, msg=a1, digestmod=SHA).digest()
    a3 = HMAC.new(secret1, msg=a2, digestmod=SHA).digest()
    h1 = HMAC.new(secret1, msg=a1+seed, digestmod=SHA).digest()
    h2 = HMAC.new(secret1, msg=a2+seed, digestmod=SHA).digest()
    h3 = HMAC.new(secret1, msg=a3+seed, digestmod=SHA).digest()
    hashSHA = h1+h2+h3[:8]
    
    a1 = HMAC.new(secret2, msg=a0).digest()
    a2 = HMAC.new(secret2, msg=a1).digest()
    a3 = HMAC.new(secret2, msg=a2).digest()
    h1 = HMAC.new(secret2, msg=a1+seed).digest()
    h2 = HMAC.new(secret2, msg=a2+seed).digest()
    h3 = HMAC.new(secret2, msg=a3+seed).digest()
    hashMD5 = h1+h2+h3
    
    xored = ''
    for x,y in zip(hashMD5,hashSHA):
        xored = xored + np.binary_repr(x^y,8)
    return xored

print('Welcome to TLS Handshake Protocol, I am Server\n')

#Create socket and bind to port and connect to client
HOST = socket.gethostname()
PORT = 1936 

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
print('Got connection from client ' + address[0] + '\nRunning handshake protocol Phase 1...\n')

#Revieve client hello
client_hello = client_socket.recv(1000000).decode()
client_parameters = client_hello.split('\n')
client_random_number = client_parameters[0]
print(f'Client Parameters\nClient Random Number: {int(client_parameters[0],2)}\nSession Id: {client_parameters[1]}\nCipher Suite: {client_parameters[2]}\n')

#Generate server hello
server_random_number = np.binary_repr(random.getrandbits(256),256)
session_id = random.randint(1,pow(2,8)) if int(client_parameters[1]) == 0 else int(client_parameters[1])
cipher_suite = client_parameters[2]
server_hello = str(server_random_number) + '\n' + str(session_id) + '\n' + cipher_suite
print(f'Server Parameters\nServer Random Number: {int(server_random_number,2)}\nSession Id: {session_id}\nCipher Suite: {cipher_suite}\n')

#Send server hello
client_socket.send(server_hello.encode())
msg = client_socket.recv(1000000).decode()
print('TLS Handshake prortocol phase 1 completed.\n')

#Generate pre master secret
print('\nNow exchanging keys (Generating pre master secret)....\n')

#Generate ephemeral Diffie Helman Parameters
p = 0 
while True:
    p = random.getrandbits(1024)    #Generate p
    if sympy.isprime(p) and p>13:
        break

g = random.randint(2,p-1)           #Generate g
b = random.randint(1,p-1)           #Server's private number b
server_public_number = pow(g,b,p)   #Server's public number g^b mod p
print(f'Generated Large Prime p: {p}\n\nPrimitive element g: {g}\n')
print(f'Server Private number: {b}\n\nServer Public number : {server_public_number}\n')
message_to_send = str(g)+' '+str(p)+' '+str(server_public_number) #Send g,p and server's public number
h = SHA.new(message_to_send.encode())                             #Generate hash of the message
print(f"Hash Digest: {codecs.encode(h.digest(),'hex').decode()}\n") #Hash Digest

#Sign using server private key
key = open('ServerPrivateKey.pem', 'rb').read()
serverprkey = RSA.importKey(key)
signer = PKCS1_v1_5.new(serverprkey)
signed_message = signer.sign(h)
print(f"Signed Hash Digest: {codecs.encode(signed_message,'hex').decode()}\n")

client_socket.send(message_to_send.encode()+b'\n\n'+signed_message)

#Receive hash digest along with client's public number, g, p
signed_message_recv = client_socket.recv(10000000)
print(f"Message Recieved from Client: {codecs.encode(signed_message_recv,'hex').decode()}\n")
msg = signed_message_recv.split(b'\n\n')
print('Now Verifying the signature .....\n')
print(f"Signature received from client: {codecs.encode(msg[1],'hex').decode()}\n")
h = SHA.new(msg[0])
print(f"Hash Digest of message received generated on server side: {codecs.encode(h.digest(),'hex').decode()}\n")

#Verify signature using client's public key
key = open('ClientPublicKey.pem', 'rb').read()
clientpkey = RSA.importKey(key)
verifier = PKCS1_v1_5.new(clientpkey)
if verifier.verify(h,msg[1]):
    print('Signature of client is authentic\n')
    gpA = msg[0].decode().split()
    client_public_number = int(gpA[2]) #Client's public number g^a mod p
    print(f'Client Public number : {client_public_number}\n')
    pre_master_secret = np.binary_repr(pow(client_public_number,b,p),1024) #Pre-master secret (g^a)^b mod p
    print(f'Pre Master Secret: {int(pre_master_secret,2)}\n')

    print('Calculating Master Secret ...\n')
    #Master secret
    label = 'Master secret'
    seed = label+client_random_number+server_random_number
    master_secret = PRF(pre_master_secret.encode(),seed.encode())
    ms = bytes(int(master_secret[i:i+8],2) for i in range(0,len(master_secret),8))
    print(f'Length of Master Secret: {len(ms)} bytes')
    print(f"Master Secret: {codecs.encode(ms,'hex').decode()}")
    
client_socket.close()
server_socket.close()


# In[ ]:




