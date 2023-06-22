import math
from itertools import product, combinations
from scipy.spatial.distance import hamming
import random
from multiprocessing import Process

def proc_c(sp, sequences, L, m):                        
    char_index = []
    for s in sequences:      
        min = m                                           
        h1 = m
        ss = ''
        for i in range(m-L+1):                          
            temp = int(hamming(sp, s[i:i+L])*L)         
            if temp < h1:
                h1 = temp
                ss = s[i:i+L]
        char_index.append((ss,h1))

        if min > h1:
            min = h1
        
    # print(char_index)
    for i in range(len(char_index)):
        if char_index[i][1] == L or i == len(char_index) - 1:
            return char_index[i]

n = int(input(f'Enter n: '))                                            # n sequences

sequences = []                                                          
substrings = []

for i in range (n):
    sequences.append(input(f'Enter sequence {i+1}: '))

L = int(input(f'Enter L: '))
m = len(sequences[0])
r = random.choice(range(1,n+1))

a = 0

for seq in sequences:
    substrings = [seq[i:i+L] for i in range(m-L+1)]
    rsubs = [list(j) for j in combinations(substrings, r)]
    
    # for each r length-L substrings of s... 
    #1-a

    for rsub in rsubs:
        print(rsub)
        #1-a
        Q = []
        for j in range(L):                 
            p = [rs[j] for rs in rsub]
            o = p.count(p[0]) == len(p)
            if (o):
                Q.append(j+1)
            d = {x:p.count(x) for x in p}
        print(Q)
        
        S = [i for i in range(1,1+L)]
        set_dif = set(S).symmetric_difference(set(Q))               # P = {1,2,...,L} - Q
        P = list(set_dif)
        
        print(P)                                        

        #1-b
        P = list(set(P))
        v1 = math.ceil((4/(2.22)**2) * math.log(n*m))
        #print(v1)

        R = []
        if len(P) != 0:
            R = random.choices(P, k = v1)
            #print(R)

        #1-c
        #i
        if len(R) != 0:
            minis = []
            for y in product('agct', repeat = len(R)):
                temp = len(P)/len(R) + 1
                for sequ in sequences:
                    substr = [sequ[b:b+L] for b in range(m-L+1)]
                    mini = ''
                    for s in substr:                       
                        y = str(y)
                        minim = hamming(y, ''.join([s[i-1] for i in R])) * len(P)/len(R) + hamming(''.join([substr[0][i-1] for i in Q]), ''.join([s[i-1] for i in Q]))
                        if minim < temp:
                            temp = minim
                            mini = s
                    minis.append(mini)
        
        #ii
        d = len(P) + len(Q)
        x = [] * len(P)
        for x_ini in product('agct', repeat = len(P)):
            x_ini = str(x_ini)
            for sequ in sequences:
                s = [sequ[b:b+len(P)] for b in range(m-len(P)+1)]
                if hamming(x_ini, ''.join([s[i-1] for i in P])) + hamming(''.join([substrings[0][i-1] for i in Q]), ''.join([s[i-1] for i in Q])) < d:
                    d = hamming(x_ini, ''.join([s[i-1] for i in R]))
                    x = str(x_ini) 
            
        #iii
        sprime = [] * len(Q)
        print(sprime)
        print(x)
        if len(Q) != 0:
            for i in P:
                sprime[i-1] = x[i-1]
            for i in Q:
                    sprime[i] = substrings[0][i]

        c = proc_c(sprime, sequences, L, m)


        a+=1

s1sub = []
for i in range(m-L+1):
    s1sub.append(sequences[0][i:i+L])
    
sth = []

for s in s1sub:
    a = proc_c(s, sequences, L, m)
    sth.append(a)

sth.sort(key=lambda x: x[0])

print(sth[0][0])