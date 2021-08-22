#!/usr/bin/env python
# coding: utf-8

# In[8]:


def ExtendedEucledian(a,b):
    if a == 0:
        return b,0,1
    ans,xa,ya = ExtendedEucledian(b%a,a)
    x = ya - (b//a)*xa
    y = xa
    return ans,x,y


# In[9]:


print('FINDING GREATEST COMMON DIVISOR AND COEFFICIENTS USING EXTENDED EUCLEDIAN ALGORITHM')
a = int(input('Enter first number '))
b = int(input('Enter second number '))
gcd,x,y = ExtendedEucledian(a,b)
print('The GCD of entered numbers is',gcd)
print('The coefficients x and y such that gcd(a,b) = ax+by are',x,'and',y)

