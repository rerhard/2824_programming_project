# Your names:
# Adam Laughlin
# Robert Erhard
#
#

# Did you copy and paste code from any online source? No

# Note: you are not allowed to do so for this assignment.
# Your answer should generally be "no". But if you did,
# mark the code clearly and explain here why you needed to do so.

# Did you collaborate with someone outside your team? No
# If yes, explain what you obtained from the collaboration.

# Did you post queries on online forums (such as stackoverflow, ..)
# related to this assignment? No
# If yes, post the links here.

#----------- IMPORTS ---------------------
from functools import reduce # for pipe
from random import randrange # to generate complexity analysis nums
from time import perf_counter,sleep # timing, and sleep for test fns
from multiprocessing import Pool,cpu_count # to run fns in different processes
from os import getpid # to check that the fns are running in different processes
from types import SimpleNamespace # dict property access is annoying
import matplotlib.pyplot as plt
import math
from math import sqrt,isclose # for fermat
# -------------------------------------------

# fn composition util
pipe = lambda fn1,*fns: lambda arg,*args: reduce(lambda a,f: f(a), fns, fn1(arg,*args))


# predicates
zero = 0.0
isNotSquare = lambda n:not isFloatZeroIsh(sqrt(n)%1)
isFloatZeroIsh = lambda n:isclose(zero,n)





# This is the brute force algorithm.
# You are being asked to improve upon this
def factorize(n):
    for i in range(2, n-1):
        if n % i == 0:
            return i
    # assert False, 'You gave me a prime number to factor'
    return -1

# Improve on factorize function above:
# Call your functions factorize1, factorize2, ...
# Please write a brief comment before each function to describe
# the improvements you are trying out.

# factorize1: Iterates only until sqrt(n) and tests only odd numbers.
def factorize1(n):
    if n % 2 == 0:
        return 2
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return i
    assert False, 'You gave me a prime number to factor'
    return -1
# Sieve: sets up a sieve of eranthoses to generate primes up to sqrt(n).
def sieve(n):
    p = int(math.sqrt(n) + 1)  # sets upper limit for list of primes
    list_primes = list(range(2, p)) # creates a list of numbers between 2 and p
    i = 2
    f = open('prime_list.txt', 'w')
    while i < p:
        if i in list_primes: # i starts at the bottom of list
            j = 2 * i # set j = smallest multiple of prime i
            while j < p:
                if j in list_primes:
                    list_primes.remove(j) # if j still in list, remove it
                j = j + i # increment j by multiples of i.
        i = i + 1 # move to the next value in the list.
    for x in list_primes: # write each prime from the list to .txt file.
        to_write = str(x) + '\n'
        f.write(to_write)
    f.close()
    return list_primes

# factorize 2: unsuccessful attempt to use a sieve combined with brute force algorithm
# to generate and utilize a list of primes in factorization process.
# unsuccessful due to collosally slow speed.
def factorize2(n):
    p = int(math.sqrt(n))
    list_primes = list(range(2, p + 1))
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


# skips some basics, then jumps by 6, only up to n/7
# I can't think of any factor that would be greater than n/7 if n%2,3,5 fail - Adam
# Could speed it up a bit by adding more tests and decreasing the loop max
def factorize4 (n):
  if(isFloatZeroIsh(n%2)):return 2;
  if(isFloatZeroIsh(n%3)):return 3;
  if(isFloatZeroIsh(n%5)):return 5;
  loopMax = int(math.ceil(n/7))
  for i in range(7,loopMax,6):
    if(isFloatZeroIsh(n%i)): return i;
    if(isFloatZeroIsh(n%(i+4))): return i+4;
  return -1;

def fermfactLoopMaxChecked(n):
    a = int(math.ceil(math.sqrt(n)))
    bsq = a ** 2 - n
    while isNotSquare(n):
        a = a + 1
        bsq = a ** 2 - n
        if(a>n): return -1
    return a - math.sqrt(bsq)


# fermfact: basic fermat factorization. Assumes n = a^2 - b^2 = (a+b)(a-b) where (a-b) is
# smallest factor. Begin testing from a = sqrt(n). bsq = a^2 - n.
# Tests bsq repeatedly to se if it is a perfect square.
# returns a - b
def fermfact(n):
    a = int(math.ceil(math.sqrt(n)))
    bsq = a ** 2 - n
    blimit = a
    while math.sqrt(bsq) != int(math.sqrt(bsq)) and math.sqrt(bsq) < blimit:
        a = a + 1
        bsq = a ** 2 - n
    if math.sqrt(bsq) == int(math.sqrt(bsq)):
        return a - math.sqrt(bsq)
    else:
        return -1

# fermfactx: tests whether removing one square root calculation improves efficiency
def fermfact2(n):
    a = int(math.ceil(math.sqrt(n)))
    bsq = a ** 2 - n
    while sqrt(bsq) % 1 != 0.0:
        a = a + 1
        bsq = a ** 2 - n
    return a - math.sqrt(bsq)

# fermfact1: basic improvement upon fermfact. Tests whether a will be even or odd
# so that a can iterate by 2.
def fermfact3(n):
    a = int(math.ceil(math.sqrt(n)))
    blimit = a
    if n % 4 == 1: # if n mod 4 = 1, a must be odd.
        if a % 2 == 0:
            a = a - 1
    if n % 4 == 3:
        if a % 2 != 0:
            a = a - 1
    bsq = a ** 2 - n
    while math.sqrt(bsq) != int(math.sqrt(bsq)) and math.sqrt(bsq) < blimit:
        a = a + 2
        bsq = a ** 2 - n
    if math.sqrt(bsq) == int(math.sqrt(bsq)):
        return a - math.sqrt(bsq)
    else:
        return -1

# unsuccessful attempt to implement pollard rho.
# we removed the imports of necessary modules after failed attempts.
def pollard_rho(n):
    x = (random.randint(1, n) % (n - 2)) + 2
    y = 0
    c = (random.randint(1, n) % (n - 1)) + 1
    d = 1
    while x != y:
        y = x
        x = (x ** 2 + c) % n
        y = (x ** 2 + c) % n
        d = fractions.gcd(abs(x - y), n)
        if d > 1:
            return d
        if d == n:
            pollard_rho(n)

# fermfact4: uses mod 10 operator to set up iterations of 'a' that are greater than 2.
# a begins at sqrt(n)
# a is determined as either odd or even
# b squared (bsq) is calculated n - a**2
# if bsq mod 10 is not in list of allowed numbers for perfect squares
# it is incremented by 2 until it does
# while bsq is not a perfect square,
# for each possible value of n mod 10, corrosponding a mod 10 values are incremented
# by their appropriate steps until bsq is a perfect square.
def fermfact4(n):
    a = int(math.ceil(math.sqrt(n)))
    bmodeven = [0, 4, 6] # list of possible even perfect bsq values
    bmododd = [1, 5, 9] # list of possible odd perfect bsq values
    bsq = a ** 2 - n
    if n % 4 == 1: # if n mod 4 is odd, a must be odd, b must be even
        if a % 2 == 0:
            a = a + 1
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                    return a - math.sqrt(bsq)
        while bsq % 10 not in bmodeven: # ensure bsq is in list of possible squares
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)): # until bsq is a perfect square
            if n % 10 == 1: # if n mod 10 = 1 and a is odd, a mod 10 can be 1, 5, 9.
                if a % 10 == 1: # this step and the following, increment a appropriately
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 5:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 10 == 9:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 3:
                if a % 10 == 3:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a + a + 6
                    bsq = a ** 2 - n
                if a % 10 == 7:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 5:
                a = a + 2
                bsq = a ** 2 - n
            if n % 10 == 7:
                if a % 10 == 1:
                    a = a + 8
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 9:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
            if n % 10 == 9:
                if a % 10 == 3:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 10 == 5:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 7:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return a - math.sqrt(bsq)
    if n % 4 == 3: # same as above, this time if n mod 4 == 3, a must be even.
        if a % 2 != 0:
            a = a + 1
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
        while bsq % 10 not in bmododd: # iterate until bsq is possible perfect square
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)):
            if n % 10 == 1:
                if a % 10 == 6:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 0:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                if a % 10 == 4:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 4
                    bsq = a ** 2 - n
            if n % 10 == 3:
                if a % 10 == 2:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a + a + 4
                    bsq = a ** 2 - n
                if a % 10 == 8:
                    a = a + 4
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
            if n % 10 == 5:
                a = a + 2
                bsq = a ** 2 - n
            if n % 10 == 7:
                if a % 10 == 4:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 8
                    bsq = a ** 2 - n
                if a % 10 == 6:
                    a = a + 8
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
            if n % 10 == 9:
                if a % 10 == 8:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 10 == 0:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 10 == 2:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
        return  a - math.sqrt(bsq)

#fermfact5: same function as fermfact4 but uses mod 16 as operator.
# turns out it is more efficient and looks like prettier code to use mod 16.
# later learned that it is convention for these sieve modulo values to be perfect squares
# hence 16 is a much more appropriate choice.
def fermfact5(n):
    a = int(math.ceil(math.sqrt(n)))
    bmodeven = [0, 4]
    bmododd = [1, 9]
    alimit = n//2
    bsq = a ** 2 - n
    if n % 4 == 1:
        if a % 2 == 0:
            a = a + 1
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                    return a - math.sqrt(bsq)
        while bsq % 16 not in bmodeven and a < alimit:
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)) and a < alimit:
            if n % 16 == 1 or n % 16 == 13:
                if a % 16 == 1 or a % 16 == 9:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                if a % 16 == 7 or a % 16 == 15:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
            if n % 16 == 9 or n % 16 == 5:
                if a % 16 == 3 or a % 16 == 11:
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                if a % 16 == 5 or a % 16 == 13:
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 6
                    bsq = a ** 2 - n
                    if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
                    a = a + 2
                    bsq = a ** 2 - n
    if math.sqrt(bsq) == int(math.sqrt(bsq)):
        return a - math.sqrt(bsq)
    if n % 4 == 3:
        if a % 2 != 0:
            a = a + 1
            bsq = a ** 2 - n
        if math.sqrt(bsq) == int(math.sqrt(bsq)):
                        return a - math.sqrt(bsq)
        while bsq % 16 not in bmododd and a < alimit:
            a = a + 2
            bsq = a ** 2 - n
            if math.sqrt(bsq) == int(math.sqrt(bsq)):
                return a - math.sqrt(bsq)
        while math.sqrt(bsq) != int(math.sqrt(bsq)) and a < alimit:
                    a = a + 4
                    bsq = a ** 2 - n
    if math.sqrt(bsq) == int(math.sqrt(bsq))and a - math.sqrt(bsq) != 1.0:
        return  a - math.sqrt(bsq)
    else:
         return -1

#
# Test Number Generation
#
def gen_nums(digits=1,samples=None,fixed_num=None):
  if(not (digits > 0)):
    digits = 1

  if(fixed_num):
    if(samples==None): return [fixed_num]
    return [fixed_num for r in range(samples)]

  min_num = 10**(digits-1)
  max_num = 10**digits
  sample_len = range(samples or int(10**(digits/2)))
  return [randrange(min_num,max_num) for s in sample_len]

# for generating large primes to test for worst case scenarios
# def genLargestPrimesOfEachDigitGroup(dmax=20,numPrimes=10,prime_check=is_probable_prime):
#   currentMax=0;
#   currentMin=0;
#   dmin=1
#   digitGroups = [];
#   d=dmax+1
#   while(d > dmin):
#     d=d-1
#     currentMax = (10**(d+1))-1;
#     currentMin = 10**d;
#     dg = [];
#     digitGroups.append(dg)
#     i=currentMax;
#     while(i>currentMin and len(dg)<numPrimes):
#       i=i-1
#       if(prime_check(i)):
#         dg.append(i);
#   digitGroups.reverse();
#   return digitGroups;

# Iteration 2, for getting worst case scenarios quickly - 20 of the largest primes in each digit group
# generated using genLargestPrimesOfEachDigitGroup, with prime_check fn from rsa_keygen
largestProbablePrimesByDigitLength = [
  [],
  [7, 5, 3, 2],
  [97, 89, 83, 79, 73, 71, 67, 61, 59, 53],
  [997, 991, 983, 977, 971, 967, 953, 947, 941, 937],
  [9973, 9967, 9949, 9941, 9931, 9929, 9923, 9907, 9901, 9887],
  [99991, 99989, 99971, 99961, 99929, 99923, 99907, 99901, 99881, 99877],
  [999983, 999979, 999961, 999959, 999953, 999931, 999917, 999907, 999883, 999863],
  [9999991, 9999973, 9999971, 9999943, 9999937, 9999931, 9999929, 9999907, 9999901, 9999889],
  [99999989, 99999971, 99999959, 99999941, 99999931, 99999847, 99999839, 99999827, 99999821, 99999787],
  [999999937, 999999929, 999999893, 999999883, 999999797, 999999761, 999999757, 999999751, 999999739, 999999733],
  [9999999967, 9999999943, 9999999929, 9999999881, 9999999851, 9999999833, 9999999817, 9999999787, 9999999781, 9999999769],
  [99999999977, 99999999947, 99999999943, 99999999907, 99999999871, 99999999851, 99999999833, 99999999829, 99999999821, 99999999769],
  [999999999989, 999999999961, 999999999959, 999999999937, 999999999899, 999999999877, 999999999863, 999999999857, 999999999847, 999999999767],
  [9999999999971, 9999999999863, 9999999999799, 9999999999763, 9999999999733, 9999999999701, 9999999999659, 9999999999643, 9999999999589, 9999999999553],
  [99999999999973, 99999999999971, 99999999999959, 99999999999931, 99999999999929, 99999999999923, 99999999999853, 99999999999829, 99999999999821, 99999999999797],
  [999999999999989, 999999999999947, 999999999999883, 999999999999877, 999999999999827, 999999999999809, 999999999999659, 999999999999643, 999999999999577, 999999999999571],
  [9999999999999937, 9999999999999917, 9999999999999887, 9999999999999851, 9999999999999817, 9999999999999809, 9999999999999671, 9999999999999643, 9999999999999641, 9999999999999631],
  [99999999999999997, 99999999999999977, 99999999999999961, 99999999999999943, 99999999999999919, 99999999999999823, 99999999999999761, 99999999999999739, 99999999999999727, 99999999999999587],
  [999999999999999989, 999999999999999967, 999999999999999877, 999999999999999863, 999999999999999829, 999999999999999749, 999999999999999737, 999999999999999709, 999999999999999637, 999999999999999631],
  [9999999999999999961, 9999999999999999943, 9999999999999999919, 9999999999999999877, 9999999999999999817, 9999999999999999751, 9999999999999999719, 9999999999999999701, 9999999999999999679, 9999999999999999673],
  [99999999999999999989, 99999999999999999973, 99999999999999999941, 99999999999999999931, 99999999999999999857, 99999999999999999803, 99999999999999999799, 99999999999999999773, 99999999999999999701, 99999999999999999689],
  [999999999999999999899, 999999999999999999887, 999999999999999999829, 999999999999999999787, 999999999999999999713, 999999999999999999683, 999999999999999999677, 999999999999999999661, 999999999999999999631, 999999999999999999571],
]





def summarizeFnTestResults(summary_list):
  summaries = {}
  for result in summary_list:
    if(not (result.name in summaries)):
      summaries[result.name] = SimpleNamespace(
        min=999999999999,
        max=0,
        mean=0,
        durations=[],
        results=[],
        name='',
        digits=len(str(result.testedNum))
      )
    summary = summaries[result.name]

    if(result.duration<summary.min):summary.min=result.duration
    if(result.duration>summary.max):summary.max=result.duration
    summary.durations.append(result.duration)
    summary.results.append(result)
    summary.name=result.name
    del result.name

  for name in summaries:
    summaries[name].mean = sum(summaries[name].durations)/len(summaries[name].durations)
    del summaries[name].durations
  [print('{} \nmean: {} \nmax: {}'.format(s.name,s.mean,s.max)) for s in summaries.values()]
  return summaries;



def execTest(tup):
  fn,num = tup;
  pid = getpid()
  print('process {}: start test {}({})'.format(pid,fn.__name__,num))
  start = perf_counter()
  output = fn(num)
  end = perf_counter()
  print('process {}: end   test {}({})=>{} with duration:{}seconds'.format(pid,fn.__name__,num,output,end-start))
  return SimpleNamespace(
    testedNum=num,
    duration=end-start,
    name=fn.__name__,
    output=output,
  )


# runs fns in parallel
def withSyncProcessPool(fn):
  def withPoolInner(lst):
    maxProcs = min([len(lst),cpu_count()]) or 1
    print(maxProcs,lst,cpu_count())
    pool = Pool(processes=maxProcs)
    result = fn(pool,lst)
    pool.close()
    pool.join()
    return result
  return withPoolInner



pairNumsWithFunctions = lambda nums: lambda *fns:[(fn,num) for num in nums for fn in fns]
execNumFunctionPairs = withSyncProcessPool(lambda pool,tups:pool.map(execTest,tups))
last = lambda arr:arr[len(arr)-1]
def computeO (last,next):
  last[0].append(abs(math.log10(abs(next[2]-last[2]*10))));
  return next;
mean = lambda arr:max(arr)

def plotSummaries(summaryList):
  legend = []
  fns = dict()
  ymax = 0
  xmax = 0
  for summary in summaryList:
    for (key,s) in summary.items():
      if(key not in fns):
        fns[key]=SimpleNamespace(xvals=[],yvals=[],name=s.name)
        legend.append(key)
      fns[key].xvals.append(s.digits)
      fns[key].yvals.append(s.max)
      if(ymax<s.max):
        ymax=s.max
      if(xmax<s.digits):
        xmax=s.digits
  # ymax = ymax+ymax/20
  plt.axis([1,xmax,0,ymax+ymax/20])
  plt.ylabel('worst case run time in seconds')
  plt.xlabel('10^n digits');
  colors=['#CC0000','#CC3333','#CC7777','#CCAAAA']
  legend.sort(key=lambda k:fns[k].yvals[len(fns[k].yvals)-1])
  legend.reverse()
  i=0

  for key in legend:
    # [math.log10(x) for x in fns[key].yvals]
    # [v for v in fns[key].yvals]

    result = []
    results = [result for v in fns[key].xvals]
    reduceArgs = list(zip(results,fns[key].xvals,fns[key].yvals))
    # proportion of numbers at one size, to numbers at the next size
    # so time1/n1, compared to time2/n2
    reduce(computeO,reduceArgs)
    print('bigO',key,reduceArgs,fns[key].xvals)
    print('bigO result',key,result)
    # print('bigO',list(zip(fns[key].xvals,fns[key].yvals)))

    plt.text(xmax-2, last(fns[key].yvals), '{} {:.5}'.format(key,last(fns[key].yvals)),color=colors[i])
    plt.plot(fns[key].xvals,fns[key].yvals,'o-',color=colors[i])
    i=i+1
  plt.show()
  return summaryList;

# var estimateBigOhs = (nAndTimePairs)=>{
#   var max=0;
#   var Ohs = nAndTimePairs.map(([n,time])=>{
#      if(typeof time !== 'number' || typeof n !== 'number'){
#        return 'all args must be nums';
#      }
#      if(n<=1){
#        return 'n must be greater than 1';
#      }
#      let result = time;
#      let o = 0;
#      while(true){
#        result = result/n;
#        o++;
#        if (result<=1){break;}
#      };
#      if(o>max){max=o;}
#      return o;
#   });
#   return {
#      ohs:Ohs,
#      ohsMax:`O(n^${max})`
#   }
# };
# estimateBigOhs([[2,4],[4,16],[8,64]])


getFnTester = lambda nums:pipe(
  pairNumsWithFunctions(nums),
  execNumFunctionPairs,
  summarizeFnTestResults
)


if __name__ == '__main__':
  #
  # # digitTesters = [getFnTester(gen_nums(digits=i,samples=100)) for i in range(1,8)]
  # # digitTesters = [getFnTester(gen_nums(fixed_num=669512017,samples=1)) for i in range(1,2)]
  twentyPrimeTests = [getFnTester(l) for l in largestProbablePrimesByDigitLength[1:]]
  singlePrimeTests = [getFnTester(l[:1]) for l in largestProbablePrimesByDigitLength[1:]]
  singlePrimeTestsTo8 = [getFnTester(l[:1]) for l in largestProbablePrimesByDigitLength[1:9]]
  plotSummaries([test(
    # factorize,
    factorize4,
    # fermfact5,
    # fermfactLoopMaxChecked
  ) for test in singlePrimeTestsTo8]);
