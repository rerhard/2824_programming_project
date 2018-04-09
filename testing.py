
import math


def sieve(n):
    p = int(math.sqrt(n) + 1)
    list_primes = list(range(2, p))
    i = 2
    f = open('prime_list.txt', 'w')
    while i < p:
        if i in list_primes:
            j = 2 * i
            while j < n:
                if j in list_primes:
                    list_primes.remove(j)
                j = j + i
        i = i + 1
    for x in list_primes:
        to_write = str(x) + '\n'
        f.write(to_write)
    f.close()
    return list_primes




import math
def factorize1(n):
    p = int(math.sqrt(n))
    list_primes = list(range(2, p))
    i = 2
    for i in list_primes:
        if n % i == 0:
            return i
        j = 2 * i
        while j < p:
            if j in list_primes:
                list_primes.remove(j)
            j = j + i
    assert False, 'You gave me a prime number to factor'
    return -1

import math
def fermfact(n):
    a = int(math.ceil(math.sqrt(n)))
    bsq = a ** 2 - n
    while math.sqrt(bsq) != int(math.sqrt(bsq)):
        a = a + 1
        bsq = a ** 2 - n
    return a - math.sqrt(bsq)
     
def fermfact1(n):
    a = int(math.ceil(math.sqrt(n)))
    if n % 4 == 1:
        if a % 2 == 0:
            a = a - 1
    if n % 4 == 3:
        if a % 2 != 0:
            a = a - 1
    bsq = a ** 2 - n
    while math.sqrt(bsq) != int(math.sqrt(bsq)):
        a = a + 2
        bsq = a ** 2 - n
    return a - math.sqrt(bsq)       
def factorize2(n):
    for i in range(2, n//2 + 1):
        if is_probable_prime(i): 
            if n % i == 0:
                return i
    assert False, 'You gave me a prime number to factor'
    return -1
import random
import random
import fractions
def pollard_rho(n):
    x = (random.randint(1, n) % (n - 2)) + 2
    y = x
    c = (random.randint(1, n) % (n - 1)) + 1
    d = 1
    while d == 1:
        x = (x ** 2 + c) % n
        y = (x ** 2 + c) % n
        d = fractions.gcd(abs(x - y), n)
        if d == n:
            pollard_rho(n)
    return d
        
pollard_rho(2605796209)    

    
def fermfact3(n):
    a = int(math.ceil(math.sqrt(n)))
    if n % 4 == 1: # a must be odd, b must be even
        if a % 2 == 0:
            a = a + 1
            asq = a ** 2
            bsq = a ** 2 - n
            p = n % 10
            q = asq % 10
            r = bsq % 10
            for r in [0, 4, 6]:
                if q == p + r and q - r == p:
                    return a - math.sqrt(bsq) 
                a = a + 10
    if n % 4 == 3: # a must be even, b must be odd
        if a % 2 != 0:
            a = a + 1
            asq = a ** 2
            bsq = a ** 2 - n
            p = n % 10
            q = asq % 10
            r = bsq % 10
            for r in [1, 5, 9]:
                if q == p + r and q - r == p:
                    return a - math.sqrt(bsq) 
                a = a + 10      



def is_probable_prime(n, s=50):
    assert n >= 2
    # special case 2
    if n == 2:
        return True
    # ensure n is odd
    if n % 2 == 0:
        return False
    # write n-1 as 2**s * d
    # repeatedly try to divide n-1 by 2
    s = 0
    d = n-1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient
    assert(2**s * d == n-1)

def list_probable_primes(n):
    f = open('prime_list.txt', 'w')
    i = 2
    while i < n:
        if is_probable_prime(i):
            x = str(i) + '\n'
            f.write(x)
        i = i + 1
    f.close()



    



            

   



