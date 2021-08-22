#!/usr/bin/env python
# coding: utf-8

# In[3]:


def EucledianGCD(a,b):
    if a == 0:
        return b
    return EucledianGCD(b%a,a)


# In[4]:


print('FINDING GREATEST COMMON DIVISOR USING EUCLEDIAN ALGORITHM')
a = int(input('Enter first number '))
b = int(input('Enter second number '))
gcd = EucledianGCD(a,b)
print('The GCD of entered numbers is',gcd)


# In[ ]:




