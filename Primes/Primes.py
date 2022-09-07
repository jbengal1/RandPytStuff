import matplotlib.pyplot as plt
import numpy as np
# Checks if a number is prime, in a very inefficient way
def stupidCheck_prime(n):
    flag = True
    for k in range(2,n):
        if (n%k==0):
            flag = False

    return flag

# Check if a given digit d appears in the string n
def checkDigitinNum(d, n):
    flag = False
    for m in str(n):
        if str(d)==m:
            flag = True
            break
    '''
    if len(str(d))==2:
        if str(d)==str(n):
            flag = True
    elif len(str(d))==3:
        if str(d)==(str(n)[0] + str(n)[1]) :
            flag = True
        elif str(d)==(str(n)[1] + str(n)[2]) :
            flag = True
    '''
    return flag

  
N_p = 110
'''
nums = np.array([k for k in range(2,N)], dtype=np.int32)
primes_ch = [stupidCheck_prime(k) for k in range(2,N)]
primes = nums[primes_ch]
'''
nums = np.array([k for k in range(2,N_p)], dtype=np.int32)
primes_ch = [stupidCheck_prime(k) for k in range(2,N_p)]
primes = nums[primes_ch]

print(primes)

# Create an data array of the counts I want to check
N = 10**5
counter = []
for p in primes:
    for num in range(2,N):
        #if checkDigitinNum(p, num):
        if num%p==0:
            counter.append(p)


# Plot histogram
counts, bins = np.histogram(counter)
print(counts)
plt.hist(bins[:-1], bins, weights=counts)
plt.grid(True)
plt.show()