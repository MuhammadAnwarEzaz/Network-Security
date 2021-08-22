#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Util.Padding import pad,unpad

def login(server_socket):
    username = input("Enter Username: ").encode()
    password = input("Enter Password: ").encode()
    server_socket.send(username+b'\n'+password)
    msg = server_socket.recv(1024)
    if msg.decode() == 'Authorised':
        print("Login Succesful")
        return True      
    else: 
        print(msg.decode())
        return False

def generate_message_to_send(aliceprkey,bobpkey):
    From = 'bob@localhost'
    To = input('To:')
    Message = input('Enter Message:')
    #Create the hash of the message
    Hash = SHA256.new(Message.encode())
    print('Hash Digest:',Hash.digest())
    #Sign Using own private key
    signer = PKCS1_v1_5.new(aliceprkey)
    signature = signer.sign(Hash)
    print(signature)
    #Concatenate the message and signature
    msg_plus_sign = Message.encode()+b'\n\n\n\n\n'+signature
    print('Message concatenated with signature:',msg_plus_sign)
    #One time secret key
    key = get_random_bytes(16)
    print('One Time Secret Key',key)
    #Encrypt using one time secret key
    aes = AES.new(key, AES.MODE_CBC)
    encrypted = aes.encrypt(pad(msg_plus_sign,AES.block_size))
    print('Encrypted Message Plus Signature using One time secret key:',encrypted)
    #Encrypt the one time secret key using reciever's public key
    rsa = PKCS1_OAEP.new(bobpkey)
    encryptedkey = rsa.encrypt(key)
    print('Encrypted one time secret key:',encryptedkey)
    #Concatenate the encrypted key with encrypted message
    msg_to_send = From.encode()+b'\n\n\n\n\n'+To.encode()+b'\n\n\n\n\n'+encryptedkey+b'\n\n\n\n\n'+aes.iv+b'\n\n\n\n\n'+encrypted
    print('Message to send:',msg_to_send)
    return msg_to_send
    
def decrypt_message(message,aliceprkey,bobpkey):
    #Separate the different parts of the message
    print('\nRecieved Message:',message)
    print('\nNow We will decrypt.....')
    splitmessage = message.split(b'\n\n\n\n\n')
    #Decrypt the secret key
    rsa = PKCS1_OAEP.new(aliceprkey)
    key = rsa.decrypt(splitmessage[2])
    print('\nOne time secret key:',key)
    print('\nAES IV:',splitmessage[3])
    #Decrypt the message
    aes = AES.new(key,AES.MODE_CBC,splitmessage[3])
    msg_sign = aes.decrypt(splitmessage[4])
    msg_plus_sign = unpad(msg_sign,AES.block_size)
    print('\nDecrypted Message (Original Message with hash digest):',msg_plus_sign)
    orgmsg = msg_plus_sign.split(b'\n\n\n\n\n')
    plaintext = orgmsg[0]
    #print('Original Encoded Message:',plaintext)
    #plaintext = unpad(orgmsg[0],AES.block_size)
    #Create the hash of the message
    Hash = SHA256.new(plaintext)
    print('\nHash Digest of Recieved Message:',Hash.digest())
    #Verify the signature
    verifier = PKCS1_v1_5.new(bobpkey)
    if (verifier.verify(Hash,orgmsg[1])):
        print("\nEmail Recieved")
        print("From : ",splitmessage[0].decode())
        print("Recieved Email: ",plaintext.decode())
    else:
        print("Signature verification unsuccessful")

key = open('BobPrivateKey.pem', 'rb').read()
bobprkey = RSA.importKey(key)

key = open('AlicePublicKey.pem', 'rb').read()
alicepkey = RSA.importKey(key)

print("I AM RECIEVER")
HOST = socket.gethostname()
PORT = 2346

client_socket = socket.socket()
print('Socket created')
print('Connecting to server...')
try:
    client_socket.connect((HOST, PORT))
except socket.error as msg:
    print ('Bind failed. Error code: ' + str(msg[0]) + ' Error message: ' + msg[1]) 
    sys.exit()

Login = login(client_socket)
if Login:
    choice = input('Do you want to send the message (Enter No Since I am reciever): ')
    if choice == 'Yes':
        msg_to_send = generate_message_to_send(bobprkey,alicepkey)
        client_socket.send(msg_to_send)
        msg = client_socket.recv(5000)
        if msg == b'You can exit':
            print('Exiting')
    else:
        msg = client_socket.recv(100000000)
        if msg == b'You can exit':
            print('Exiting...')
        else:
            decrypt_message(msg,bobprkey,alicepkey)
        client_socket.close()
else:
    print(" ")
client_socket.close()


# In[ ]:




