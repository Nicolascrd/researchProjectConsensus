import math

# constants
k = 2  # how many requests per group of request
n = 5  # number of nodes
table = []  # Probabilities : table[i][j] probability of i colored states, j groups of requests
# table contains -1 if the probability was not yet computed
for i in range(n+1):
    if i == 0:
        table.append([0 for i in range(n+1)])
    else:
        table.append([])
        for j in range(n+1):
            table[i].append(-1)


table[1][1] = 1 # one node receives the information and emits one group of requests
print(table)


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

    if table[c][reqs] != -1:
        return table[c][reqs]
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


table[2][1] = Pcreqs(2, 1)
table[3][1] = Pcreqs(3, 1)
table[4][1] = Pcreqs(4, 1)
table[5][1] = Pcreqs(5, 1)
table[2][2] = Pcreqs(2, 2)
table[3][2] = Pcreqs(3, 2)
table[4][2] = Pcreqs(4, 2)
table[5][2] = Pcreqs(5, 2)
print(table)
