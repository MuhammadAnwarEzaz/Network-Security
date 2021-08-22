#!/usr/bin/env python
# coding: utf-8

# In[24]:


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

print('Welcome to TLS Handshake Protocol, I am Client')

#Create socket and connect to client
HOST = socket.gethostname()
PORT = 1936

client_socket = socket.socket()
print('\nSocket created')
print('Connecting to server...')
try:
    client_socket.connect((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()
    
print('Socket bind complete. \nRunning handshake protocol Phase 1...')

#Generate client hello
client_random_number = np.binary_repr(random.getrandbits(256),256)
session_id = random.choice([0,random.getrandbits(8)])
cipher_suite = 'TLS_DHE_RSA_WITH_DES_CBC_SHA'
client_hello = client_random_number + '\n' + str(session_id) + '\n' + cipher_suite
print(f'Client Parameters\nClient Random Number: {int(client_random_number,2)}\nSession Id: {session_id}\nCipher Suite: {cipher_suite}\n')

#Send client hello
client_socket.send(client_hello.encode())

#Recieve server hello
server_hello = client_socket.recv(1000000).decode()
server_parameters = server_hello.split('\n')
server_random_number = server_parameters[0]
print(f'Server Parameters\nServer Random Number: {int(server_parameters[0],2)}\nSession Id: {server_parameters[1]}\nCipher Suite: {server_parameters[2]}\n')
client_socket.send('.............'.encode())
print('TLS Handshake protocol phase 1 completed.\n')

#Generate pre-master secret
print('\nNow exchanging keys (Generating pre master secret)....\n')

#Recieve g,p and server's public number
signed_message_recv = client_socket.recv(10000000)
print(f"Message Recieved from Server: {codecs.encode(signed_message_recv,'hex').decode()}\n")
msg = signed_message_recv.split(b'\n\n')
print('Now Verifying the signature .....\n')
print(f"Signature received from server: {codecs.encode(msg[1],'hex').decode()}\n")
h = SHA.new(msg[0])
print(f"Hash Digest of message received generated on client side: {codecs.encode(h.digest(),'hex').decode()}\n")

#Verify the signature using server's public key
key = open('ServerPublicKey.pem', 'rb').read()
serverpkey = RSA.importKey(key)
verifier = PKCS1_v1_5.new(serverpkey)
if verifier.verify(h,msg[1]):
    print('Signature of server is authentic\n')
    gpB = msg[0].decode().split()
    #Ephemeral Diffie Hellman parameters
    g = int(gpB[0])     #Primitive element g
    p = int(gpB[1])     #Prime number of 
    server_public_number = int(gpB[2]) #Server's public number g^b mod p
    print(f'Generated Large Prime p: {p}\n\nPrimitive element g: {g}\n\nServer Public number : {server_public_number}\n')
    a = random.randint(1,p-1)          #Client's private number
    client_public_number = pow(g,a,p)  #Client's public number g^a mod p
    print(f'Client Private number: {a}\n\nClient Public number : {client_public_number}\n')
    
    pre_master_secret = np.binary_repr(pow(server_public_number,a,p),1024)   #Pre-master secret (g^b)^a mod p
    print(f'Pre Master Secret: {int(pre_master_secret,2)}\n')
    
    message_to_send = str(g)+' '+str(p)+' '+str(client_public_number) #Send g,p and server's public number
    h = SHA.new(message_to_send.encode())                             #Generate hash of the message
    print(f"Hash Digest: {codecs.encode(h.digest(),'hex').decode()}\n") #Hash Digest
    
    #Sign using client's private key
    key = open('ClientPrivateKey.pem', 'rb').read()
    clientprkey = RSA.importKey(key)
    signer = PKCS1_v1_5.new(clientprkey)
    signed_message = signer.sign(h)
    print(f"Signed Hash Digest: {codecs.encode(signed_message,'hex').decode()}\n")
    
    client_socket.send(message_to_send.encode()+b'\n\n'+signed_message)
    
    print('Calculating Master Secret ...\n')
    #Master secret
    label = 'Master secret'
    seed = label+client_random_number+server_random_number
    master_secret = PRF(pre_master_secret.encode(),seed.encode())
    ms = bytes(int(master_secret[i:i+8],2) for i in range(0,len(master_secret),8))
    print(f'Length of Master Secret: {len(ms)} bytes')
    print(f"Master Secret: {codecs.encode(ms,'hex').decode()}")

client_socket.close()


# In[ ]:




