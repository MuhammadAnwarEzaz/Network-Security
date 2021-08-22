#!/usr/bin/env python
# coding: utf-8

# # SQUARE AND MULTIPLY ALGORITHM

# In[5]:


def square_and_multiply(base,exponent,modulus):
    exp = bin(exponent)[2:]
    modresult, result, num_squares, num_multiply = 1, 1, 0, 0
    for x in exp:
        modresult, result, num_squares = (modresult**2)%modulus, result**2, num_squares+1
        if int(x) == 1:
            modresult, result, num_multiply = (modresult*base)%modulus, result*base, num_multiply+1 
    return result, modresult, num_squares, num_multiply


# In[2]:


print('SQUARE AND MULTIPLY ALGORITHM')
a = int(input('Enter the base a: '))
b = int(input('Enter the exponent b: '))
n = int(input('Enter the modulus n: '))


# In[6]:


res, modres, numsq, nummul = square_and_multiply(a,b,n)
print('Nummber of Squares =',numsq)
print('Number of Multiplications = ',nummul)
print('Exponentiation Result = a^b =',res)
print('Modular Exponentiation Result = a^b mod n =',modres)

