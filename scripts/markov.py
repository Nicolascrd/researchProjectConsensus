import math
import numpy as np

# constants
k = 12  # how many requests per group of request
n = 20  # number of nodes

# Probabilities : array[i][j] probability of i colored states, j groups of requests
array = np.ndarray(shape=(n+1, n+1), dtype=float)
array.fill(-1)  # table contains -1 if the probability was not yet computed

for i in range(n+1):
    array[0][i] = 0

array[1][1] = 1  # one node receives the information and emits one group of requests
print(array)


def Pcreqs(c, reqs):
    print("requested proba of " + str(c) + " colored nodes and " +
          str(reqs) + " groups of requests")
    res = 0
    if c < 1:
        return 0
    if c > n:
        return 0
    if reqs > c:
        return 0
    if reqs < 0:
        return 0

    if array[c][reqs] != -1:
        return array[c][reqs]
    for t in range(k+1):
        if 0 > k-t or k-t > c-t-1:
            continue
        if 0 > t or 0 > n-c:
            continue
        if 0 > k or k > n-1:
            continue

        if reqs + 1 - t > 0: # no requests can't progress
            res += math.comb(n-c+t, t) * math.comb(c-t-1, k-t) * \
                Pcreqs(c-t, reqs+1-t)
    ans = res / math.comb(n-1, k)
    array[c][reqs] = ans
    return ans


for i in range(1, n+1):
    for j in range(n+1):
        array[i][j] = Pcreqs(i, j)


print(array)

sumNoRequests = 0

for i in range(0, n+1):
    sumNoRequests += array[i][0]

print("SUM", sumNoRequests)