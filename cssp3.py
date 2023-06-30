import math
from itertools import product, combinations
from scipy.spatial.distance import hamming
import random
import multiprocessing
from multiprocessing import Process
from joblib import Parallel, delayed
from tqdm import tqdm
import time

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
        
    for i in range(len(char_index)):
        if char_index[i][1] == L or i == len(char_index) - 1:
            return char_index[i]

def main():
    n = int(input(f'Enter n: '))                                            
    sequences = []                                                          
    substrings = []

    for i in range (n):                                                     
        sequences.append(input(f'Enter sequence {i+1}: '))                  

    L = int(input(f'Enter L: '))                                            
    m = len(sequences[0])                                                   
    r = random.choice(range(1,n+1))                                         
    print(r)    

    a = 0

    ss1 = []

    start_time = time.time()

    for seq in sequences:
        substrings = [seq[i:i+L] for i in range(m-L+1)]
        rsubs = [list(j) for j in combinations(substrings, r)]
        
        # for each r length-L substrings of s... 
        #1-a

        for rsub in rsubs:
            #1-a
            Q = []
            for j in range(L):                 
                p = [rs[j] for rs in rsub]
                o = p.count(p[0]) == len(p)
                if (o):
                    Q.append(j+1)
                d = {x:p.count(x) for x in p}
            
            S = [i for i in range(1,1+L)]
            set_dif = set(S).symmetric_difference(set(Q))               
            P = list(set_dif)
                                    

            #1-b
            P = list(set(P))
            v1 = math.ceil((4/(2.22)**2) * math.log(n*m))
            #print(v1)

            R = []
            if len(P) != 0:
                R = random.choices(P, k = v1)

            #1-c
            if len(R) != 0:
                minis = []
                for y in product('agct', repeat = len(R)):
                    #i
                    y = ''.join([str(c) for c in list(y)])
                    temp = len(P)/len(R) + 1
                    for sequ in sequences:
                        substr = [sequ[b:b+L] for b in range(m-L+1)]
                        mini = ''
                        for s in substr:      
                            minim = hamming(y, ''.join([s[i-1] for i in R])) * len(P)/len(R) + hamming(''.join([substr[0][i-1] for i in Q]), ''.join([s[i-1] for i in Q]))
                            if minim < temp:
                                temp = minim
                                mini = s
                        minis.append(mini)
            
                    #ii
                    d = len(P) + len(Q)
                    x = [] * len(P)
                    if len(P) != 0 and len(Q) != 0:
                        for x_ini in product('agct', repeat = L):
                            x_p = ''.join([str(y) for y in list(x_ini)])
                            for sequ in sequences:                        
                                if hamming(x_p, ''.join([sequ[i-1] for i in P])) + hamming(''.join([substrings[0][i-1] for i in Q]), ''.join([sequ[i-1] for i in Q])) < d:
                                    d = hamming(x_p, ''.join([sequ[i-1] for i in P])) + hamming(''.join([substrings[0][i-1] for i in Q]), ''.join([sequ[i-1] for i in Q]))
                                    x = x_p
                        
                    #iii
                    if len(Q) != 0:
                        sprime = 'a'
                        sprime = list(sprime * L)
                        for i in P:
                            sprime[i-1] = x[i-1]
                        for i in Q:
                            sprime[i-1] = substrings[0][i-1]

                        sprime = ''.join([str(y) for y in sprime])

                        c = proc_c(sprime, sequences, L, m)
                        ss1 = c

                        a+=1

    s1sub = []
    for i in range(m-L+1):
        s1sub.append(sequences[0][i:i+L])
        
    ss2 = []

    for s in s1sub:
        a = proc_c(s, sequences, L, m)
        ss2.append(a)

    ss2.sort(key=lambda x: x[0])

    if len(ss1) != 0:
        if ss2[0][1] < ss1[1]:
            print(ss2[0][0])
        else:
            print(ss1[0])
    else:
        print(ss2[0][0])

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()