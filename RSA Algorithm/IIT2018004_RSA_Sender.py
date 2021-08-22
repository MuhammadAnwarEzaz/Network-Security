#!/usr/bin/env python
# coding: utf-8

# # RSA ENCRYPTION (CLIENT / SENDER)

# **Utility**

# In[ ]:


print('Hello. This is Message Encrypter/Message Sender.')
def square_and_multiply(base,exponent,modulus):
    exp = bin(exponent)[2:]
    modresult = 1
    for x in exp:
        modresult = (modresult**2)%modulus
        if int(x) == 1:
            modresult = (modresult*base)%modulus 
    return modresult


# **Create Socket and Connect to Reciever**

# In[ ]:


import socket,sys

HOST = socket.gethostname()
PORT = 2547

client_socket = socket.socket()
print('\nSocket created')
print('Connecting to server...')
try:
    client_socket.connect((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()
    
print('Connected to Server')


# **Recieve Keys from Server**

# In[ ]:


keys = client_socket.recv(4096).decode()
print('\nRecieved Keys from Server')
temp = keys.split('\n')
base = int(temp[0])
block_size = int(temp[1])
n = int(temp[2])
e = int(temp[3])
print(f'Block Size: {block_size}')
print(f'n = {n}')
print(f'Public Key (Encryption Key): e = {e}')


# **Message Input**

# In[ ]:


message = input('Enter the message to be encrypted: ')


# **Conversion of Message Blocks to Numbers**

# In[ ]:


split_message = []
encoded_message = []
for i in range(0,len(message),block_size):
    block = message[i:i+block_size]
    split_message.append(block)
    encoded_message.append(sum([ord(block[j])*(base**(len(block)-j-1)) for j in range(len(block))]))
    
print(f'\nMessage split into blocks:\n{split_message}')
print(f'\nPlaintext represented as numbers:\n{encoded_message}')


# **Encryption**

# In[ ]:


print('\nNow Encrypting')
ciphertext = []
for block in encoded_message:
    encrypted_block = square_and_multiply(block,e,n)
    ciphertext.append(encrypted_block)
    
print(f'Ciphertext represented as numbers:\n{ciphertext}')


# **Send the Ciphertext to Receiver**

# In[ ]:


print('\nSent Ciphertext to Reciever')
cipher = str(ciphertext[0])
for i in range(1,len(ciphertext)):
    cipher = cipher + ' ' + str(ciphertext[i])
client_socket.send(cipher.encode())


# **Close the Connection**

# In[ ]:


client_socket.close()

