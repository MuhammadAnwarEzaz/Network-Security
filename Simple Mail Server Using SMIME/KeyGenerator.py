#!/usr/bin/env python
# coding: utf-8

# In[1]:


from Crypto.PublicKey import RSA
from Crypto import Random

random_generator = Random.new().read
keys = RSA.generate(1024, random_generator)
file = open('AlicePrivateKey.pem', 'wb')
file.write(keys.exportKey('PEM'))
file.close()
file = open('AlicePublicKey.pem', 'wb')
file.write(keys.publickey().exportKey('PEM'))
file.close()

keys = RSA.generate(1024, random_generator)
file = open('BobPrivateKey.pem', 'wb')
file.write(keys.exportKey('PEM'))
file.close()
file = open('BobPublicKey.pem', 'wb')
file.write(keys.publickey().exportKey('PEM'))
file.close()


# In[ ]:




