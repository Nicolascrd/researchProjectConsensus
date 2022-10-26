import math
import numpy as np

# constants
k = 3  # how many requests per group of request
n = 10  # number of nodes

# Probabilities : array[i][j] probability of i colored states, j groups of requests
array = np.ndarray(shape=(n, n), dtype=float)
array.fill(-1)  # table contains -1 if the probability was not yet computed

for i in range(n):
    array[0][i] = 0

array[1][1] = 1  # one node receives the information and emits one group of requests
print(array)


def Pcreqs(c, reqs):
    print("requested proba of " + str(c) + " colored nodes and " +
          str(reqs) + " groups of requests")
    res = 0
    if c == n:
        print("all nodes colored")
    if reqs == 0:
        print("end: no requests")
    if c < 1:
        print("less than 1 colored nodes : impossible")
        return 0
    if c > n:
        print("more colored nodes than nodes: impossible")
        return 0
    if reqs > c:
        print("more group of requests than colored nodes: impossible")
        return 0
    if reqs < 0:
        print("less than 0 requests: impossible")
        return 0

    if array[c][reqs] != -1:
        return array[c][reqs]
    for t in range(k+1):
        if 0 > k-t or k-t > c-t-1:
            return 0
        if 0 > t or 0 > n-c:
            return 0
        if 0 > k or k > n-1:
            return 0
        res += math.comb(n-c+t, t) * math.comb(c-t-1, k-t) * \
            Pcreqs(c-t, reqs+1-t)
    return res / math.comb(n-1, k)


for i in range(1, n):
    for j in range(n):
        array[i][j] = Pcreqs(i, j)

print(array)
