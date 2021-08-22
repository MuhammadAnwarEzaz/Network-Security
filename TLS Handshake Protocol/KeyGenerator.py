#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Crypto.PublicKey import RSA
from Crypto import Random

random_generator = Random.new().read
keys = RSA.generate(1024, random_generator)
file = open('ClientPrivateKey.pem', 'wb')
file.write(keys.exportKey('PEM'))
file.close()
file = open('ClientPublicKey.pem', 'wb')
file.write(keys.publickey().exportKey('PEM'))
file.close()

keys = RSA.generate(1024, random_generator)
file = open('ServerPrivateKey.pem', 'wb')
file.write(keys.exportKey('PEM'))
file.close()
file = open('ServerPublicKey.pem', 'wb')
file.write(keys.publickey().exportKey('PEM'))
file.close()

