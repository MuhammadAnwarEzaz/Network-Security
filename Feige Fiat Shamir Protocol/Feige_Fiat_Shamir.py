import random
import time

nobn = 512
nobk = 10
sl = 2

def eucledianGCD(a,b):
    if a == 0:
        return b
    return eucledianGCD(b%a,a)

def squareAndMultiply(a,b,n):
    y = bin(int(b))
    x = 1
    for i in range(2,len(y)):
        x = (x*x)%n
        if int(y[i]) == 1:
            x = (x*a)%n
    return x

def millerRabinPrimalityTest(n,k):
    d = n-1
    r = 0
    while d%2==0:
        d = d//2
        r = r+1
    d = int(d) 
    flag = 0
    for i in range(k):
        a = random.randint(2,n-2)
        x = squareAndMultiply(a,d,n)
        if x == 1 or x == n-1:
            continue
        
        for j in range(r-1):
            flag = 0
            x = ((x%n)*(x%n))%n
            if x == n-1:
                flag = 1
                break
        if flag == 1:
            continue
        return False
    return True

class Peggy:
    def __init__(self,k):
        self.k = k
        self.p = 0
        self.q = 0
        self.S = []
        self.sgn = 0
        self.r = 0
        
    def generatePrimes(self):
        print("\nGenerating two large primes p and q ...")
        while True:
            self.p = random.getrandbits(nobn)
            i = random.getrandbits(nobk)
            if self.p>3 and i>0 and millerRabinPrimalityTest(self.p,i):
                break
    
        while True:
            self.q = random.getrandbits(nobn)
            i = random.getrandbits(nobk)
            if self.q>3 and i>0 and millerRabinPrimalityTest(self.q,i) and self.q != self.p:
                break
                
        print("Two primes are p = "+str(self.p)+" q = "+str(self.q))
        N = self.p*self.q
        print("N = "+str(N))
        return N
    
    def generatePrivateKey(self,N):
        print("\nGenerating private key of Peggy ...")
        for i in range(self.k):
            x = 0
            while True:
                x = random.randint(1,N-1)
                if x<N and eucledianGCD(x,N) == 1 and x not in self.S:
                    break
            self.S.append(x)
        print("Private Key of Peggy = "+str(self.S))
    
    def generatePublicKey(self,N):
        print("\nGenerating public key of Peggy ...")
        V = []
        for i in range(self.k):
            v = (self.S[i]*self.S[i])%N
            V.append(v)
        print("Public Key of Peggy = "+str(V))
        return V
    
    def generateX(self,N):
        print("\nGenerating X = s*r^2 mod N")
        self.r = random.randint(1,N-1)
        self.sgn = self.sgn = random.choice((-1,1))
        X = (self.sgn * (((self.r%N)*(self.r%N))%N))%N
        print("r = "+str(self.r))
        print("sgn = "+str(self.sgn))
        print("X = "+str(X))
        return X
        
    def computeY(self,Ai,N):
        print("\nComputing Y = r*((s1)^a1)*((s2)^a2)*...*((sk)^ak) mod N")
        Y = self.r
        for i in range(self.k):
            if Ai[i] != 0:
                Y = (Y*self.S[i])%N
        print("Y = "+str(Y))
        return Y
    
class Victor:
    def __init__(self,k):
        self.k = k 
        
    def generateChallenge(self):
        print("\nGenerating challenge key ...")
        Ai = []
        for i in range(self.k):
            a = random.getrandbits(1)
            Ai.append(a)
        print("A = "+str(Ai))
        return Ai
    
    def check(self, Y, X, A, N, V):
        print("\nChecking y^2 = +-x*((v1)^a1)*((v2)^a2)*...*((vk)^ak) mod N and x =/= 0")
        Y_square_n = (Y*Y)%N
        temp1 = 1
        temp2 = -1
        for i in range(self.k):
            if A[i] != 0:
                temp1 = (temp1*V[i])%N
                temp2 = (temp2*V[i])%N
        temp1 = (temp1*X)%N
        temp2 = (temp2*X)%N
        
        print("y^2 mod N = "+str(Y_square_n))
        print("x*((v1)^a1)*((v2)^a2)*...*((vk)^ak) mod N = "+str(temp1))
        print("-x*((v1)^a1)*((v2)^a2)*...*((vk)^ak) mod N = "+str(temp2))
        
        if (Y_square_n == temp1 or Y_square_n == temp2) and X != 0:
            return True
        return False
    
def main():
    k = int(input("Enter the value of k (Length of Secret): "))
    t = int(input("Enter the value of t (Number of Iterations): "))
    peggy = Peggy(k)
    N = peggy.generatePrimes()
    time.sleep(sl)
    peggy.generatePrivateKey(N)
    time.sleep(sl)
    V = peggy.generatePublicKey(N)
    time.sleep(sl)
    victor = Victor(k)
    flag = 1
    
    for i in range(t):
        print("\nIteration Number = "+str(i+1))
        X = peggy.generateX(N)
        time.sleep(sl)
        A = victor.generateChallenge()
        time.sleep(sl)
        Y = peggy.computeY(A,N)
        time.sleep(sl)
        res = victor.check(Y,X,A,N,V)
        time.sleep(sl)
        if res == False:
            flag = 0
            break
    if flag == 1:
        print("\nPeggy Passed")
    else:
        print("\nPeggy Lied")

main()