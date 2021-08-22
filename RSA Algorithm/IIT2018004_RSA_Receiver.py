#!/usr/bin/env python
# coding: utf-8

# # RSA KEY GENERATION AND DECRYPTION (SERVER / RECIEVER)

# **Block Size Input**

# In[1]:


print('Hello. This is Key Generator/Message Receiver.')
block_size = int(input('Enter the size of block: '))


# **Utilities**

# In[3]:


def ExtendedEucledian(a,b):
    if a == 0:
        return b,0,1
    ans,xa,ya = ExtendedEucledian(b%a,a)
    x = ya - (b//a)*xa
    y = xa
    return ans,x,y

def square_and_multiply(base,exponent,modulus):
    exp = bin(exponent)[2:]
    modresult = 1
    for x in exp:
        modresult = (modresult**2)%modulus
        if int(x) == 1:
            modresult = (modresult*base)%modulus 
    return modresult


# **Key Generation**

# In[4]:


import numpy as np
import random
import sympy as sp

base = 256  #The message can containg any ASCII character
print('Generating Keys\n')
max_message_value = (base**block_size)-1        #The message can contain any of ASCII characters
root_n = int(np.ceil(np.sqrt(max_message_value)))

p = 137
q = 131
n = p*q

#Generate p and q
while n < max_message_value:
    while True:
        p = random.getrandbits(len(bin(root_n)[2:]))
        if sp.isprime(p):
            break
    while True:
        q = random.getrandbits(len(bin(root_n)[2:]))
        if sp.isprime(q) and q != p:
            break
    n = p*q

#Find Phi(n) 
phi_n = (p-1)*(q-1)

e = 3
d = 11787

#Generate public and private keys
while True:
    while True:
        e = random.randint(2,phi_n-1)
        gcd,x,y = ExtendedEucledian(e,phi_n)
        if gcd == 1:
            break
    d = (x%phi_n+phi_n)%phi_n
    if e != d:
        break
print('Generated Keys\n')
print(f'Generated primes: p = {p} and q = {q}')
print(f'n = pxq = {n}')
print(f'phi(n) = (p-1)x(q-1) = {phi_n}')
print(f'Public Key: e = {e}')
print(f'Private Key: d = {d}')


# **Creating Socket and Connecting to Sender**

# In[8]:


import socket,sys

HOST = socket.gethostname()
PORT = 2547

server_socket = socket.socket()
print('\nSocket created')

try:
    server_socket.bind((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()

print('Socket bind complete')
server_socket.listen(5)
print('Socket now listening')

(client_socket, address) = server_socket.accept()    
print('Got connection from client ' + address[0] + '.')


# **Send Public Parameters to Sender**

# In[ ]:


keys = str(base)+'\n'+str(block_size)+'\n'+str(n)+'\n'+str(e)
client_socket.send(keys.encode())
print('Sent Public Key to Sender')


# **Recieve the Ciphertext from Sender**

# In[ ]:


cipher = client_socket.recv(4096).decode()
print('\nRecieved Ciphertext from Sender')
cipher = cipher.split(' ')
ciphertext = []
for x in cipher:
    ciphertext.append(int(x))
    
print(f'Ciphertext represented as numbers:\n{ciphertext}')


# **Decryption**

# In[6]:


print('\nNow Decrypting')
plaintext = []
for block in ciphertext:
    decrypted_block = square_and_multiply(block,d,n)
    plaintext.append(decrypted_block)
    
print(f'Plaintext represented as numbers:\n{plaintext}')


# **Conversion of Integer Plaintext to Message**

# In[7]:


message = ''
for x in plaintext:
    block = ''
    num = x
    while(num != 0):
        block = chr(num%base)+block
        num = num//base
    message = message+block

print('\nOriginal Message sent by Sender:\n'+message)


# **Close the Connection**

# In[ ]:


client_socket.close()
server_socket.close()

