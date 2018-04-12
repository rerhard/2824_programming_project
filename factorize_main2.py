# Your names:
#
#
#
#

# Did you copy and paste code from any online source?

# No. Pollard Rho function here referenced (but not copied) some code at 
# http://josephlemley.com/blog/pollards-rho-algorithm-for-fast-factorization-in-python/
# and https://www.geeksforgeeks.org/pollards-rho-algorithm-prime-factorization/
# but our function was unsuccessful and so we pursued Fermat's algorithm instead.
# Included our Pollard Rho fn to show our attempt. 

# Note: you are not allowed to do so for this assignment.
# Your answer should generally be "no". But if you did,
# mark the code clearly and explain here why you needed to do so.

# Did you collaborate with someone outside your team? No. 
# If yes, explain what you obtained from the collaboration.

# Did you post queries on online forums (such as stackoverflow, ..)
# related to this assignment? No. 
# If yes, post the links here.

#----------- IMPORTS ---------------------

# If you have import statements, please explain in comments
# why you need them. You can be very brief.

from __future__ import print_function
# I import this just for compatibility with python2 please use python3
# though.

import sys
import math
from math import sqrt
# sys has useful utilities I need.




from time import clock as time_clock
# Time is being imported to measure
# running time for the factorize
# function.

from functools import reduce # for pipe
from random import randrange # to generate complexity analysis nums
from time import perf_counter,sleep # timing, and sleep for test fns
from multiprocessing import Pool # to run fns in different processes
from os import getpid # to check that the fns are running in different processes
from types import SimpleNamespace # dict property access is annoying

# -------------------------------------------

# fn composition ltr
pipe = lambda fn1,*fns: lambda arg,*args: reduce(lambda a,f: f(a), fns, fn1(arg,*args))


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



def gen_nums(digits=1,samples=None,fixed_num=None):
  if(digits < 1):
    digits = 1

  if(fixed_num):
    if(samples==None): return [fixed_num]
    return [fixed_num for r in range(samples)]

  min_num = 10**(digits-1)
  max_num = 10**digits
  sample_len = range(samples or int(10**(digits/2)))
  return [randrange(min_num,max_num) for s in sample_len]

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
  # return summaries

def execTest(tup):
  fn,num = tup;
  pid = getpid()
  print('process {}: start test {}({})'.format(pid,fn.__name__,num))
  start = perf_counter()
  output = fn(num)
  end = perf_counter()
  print('process {}: end   test {}({})=>{} with duration:{}ms'.format(pid,fn.__name__,num,output,end-start))
  return SimpleNamespace(
    testedNum=num,
    duration=end-start,
    name=fn.__name__,
    output=output,
  )

def withSyncProcessPool(fn):
  def withPoolInner(*args,**kwargs):
    pool = Pool()
    result = fn(pool,*args,**kwargs)
    pool.close()
    pool.join()
    return result
  return withPoolInner

pairNumsWithFunctions = lambda nums: lambda *fns:[(fn,num) for num in nums for fn in fns]
execNumFunctionPairs = withSyncProcessPool(lambda pool,tups:pool.map(execTest,tups))
def plotSummaries(summaryList):
  return summaryList;

getFnTester = lambda nums:pipe(
  pairNumsWithFunctions(nums),
  execNumFunctionPairs,
  summarizeFnTestResults
)



# Below we have test code:
# to test your function say factorize2, you would simply call
if __name__ == '__main__':
  digitTesters = [getFnTester(gen_nums(digits=i,samples=1)) for i in range(1,7)]
  summaries = plotSummaries([tester(factorize) for tester in digitTesters])
  [print(s) for s in summaries]
  # fermfact(716550)
#     # First parse command line arguments and figure out which
#     # function we want to test
#     if len(sys.argv) <= 1:
#         fun = fermfact5
#     else:
#         fun_to_call_string = sys.argv[1]
#         assert fun_to_call_string in globals(), ('You did not implement '+fun_to_call_string)
#         globals_copy= globals().copy()
#         fun = globals_copy.get(fun_to_call_string)
#     # Open the file with list of numbers
#     # test_7digit_fixed_prime = execTests(gen_nums(fixed_num=5515927,samples=5))
#     # test_7digit_fixed_prime(factorize,factorize1)
#
#     f = open('composite_list.txt', 'r')
#     # test each number
#     for line in f:
#         n = int(line)
#         print('Factoring', n, '(', len(line), 'digits ): ', end='')
#         time_elapsed = execTests([n])(fun)
# #         t1 = time_clock() # Record time
# #         p = fun(n)
# #         t2 = time_clock() # Record time
# #         time_elapsed = t2 - t1  # seconds
#         print('Factor = ', p, ' other factor = ', n/p, ' Time Elapsed: ', time_elapsed)
#         if n % p != 0:
#             print('Factorization failed for: ', n)
#             sys.exit(1)
#     f.close()