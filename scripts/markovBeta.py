# Compute probabilities with Beta = 2

import math
import numpy as np
import sys
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# constants
# k = 8  # how many requests per group of request
# n = 30   # number of nodes

# Probabilities : array[i][j][k][l] probability of i colored nodes, j semi-colored nodes, k requests from colored nodes, l requests from semi-colored nodes

# array = np.ndarray(shape=(n+1, n+1, n+1, n+1), dtype=float)
# array.fill(-1)  # table contains -1 if the probability was not yet computed

# # one node receives the information and emits one group of requests
# array[0][1][0][1] = 1
# print(array)


# for i in range(n+1):
#     for j in range(n+1):
#         for u in range(n+1):
#             for v in range(n+1):
#                 array[i][j][u][v] = Pcreqs(i, j, u, v)

# print(Pcreqs(0, 4, 0, 3))
# print(Pcreqs(3, 1, 3, 2))
# print(array)

# sumNoRequests = 0
# noConsensus = 0

# for i in range(0, n+1):
#     for j in range(0, n+1):
#         sumNoRequests += array[i][j][0][0]
#         if i+j != n:
#             noConsensus += array[i][j][0][0]

# print("SUM", sumNoRequests)
# print("no consensus", noConsensus)


def getNoConsensusProb(n, k):

    # n number of nodes
    # k number of requests per round
    array = np.ndarray(shape=(n+1, n+1, n+1, n+1), dtype=float)
    array.fill(-1)  # table contains -1 if the probability was not yet computed

    # one node receives the information and emits one group of requests
    array[0][1][0][1] = 1

    def Pcreqs(c, s, reqsc, reqss):
        # print("requested proba of " + str(c) + " colored nodes, " + str(s) + " semi colored nodes, " + str(reqsc) + " groups of requests from colored nodes and " +
        #     str(reqss) + " groups of requests from semi-colored nodes")
        if c + s < 1:
            return 0
        if c < 0:
            return 0
        if c+s > n:
            return 0
        if s < 0:
            return 0
        if reqsc > c:
            return 0
        if reqsc < 0:
            return 0
        if reqss > s+c:
            return 0
        if reqss < 0:
            return 0

        if array[c][s][reqsc][reqss] != -1:
            # print(
            #     "P(" + " ".join([str(c), str(s), str(reqsc), str(reqss)]) + ") = " + str(array[c][s][reqsc][reqss]))
            return array[c][s][reqsc][reqss]

        # considering a step with a group of requests from a semi-colored node
        # print("considering a step with a group from sm node")
        ress = 0
        for tv in range(k+1):
            for ts in range(k+1):
                if n-c-s+ts+tv < tv:
                    continue
                if s-tv-1+ts < ts:
                    continue
                if k-tv-ts > c-ts:
                    continue
                if c-ts < 0:
                    continue
                if s-tv-1 < 0:
                    continue
                if n-c-s+ts+tv < 0:
                    continue
                if k - tv-ts < 0:
                    continue
                if reqss+1-tv < 0:
                    continue
                if reqsc-ts < 0:
                    continue

                if reqss + 1 - tv > 0:  # no requests can't progress
                    ress += math.comb(n-c-s+tv, tv) * math.comb(s-tv-1+ts, ts) * \
                        math.comb(c-ts, k-tv-ts) * Pcreqs(c-ts,
                                                          s-tv+ts, reqsc-ts, reqss+1-tv)

        # considering a step with a group of requests from a colored node
        # print("considering a step with a group from colored node only if no groups of requests from semi colored nodes")
        resc = 0
        for tv in range(k+1):
            if reqss != tv:
                # no requests from semi colored nodes
                continue
            for ts in range(k+1):
                if n-c-s+ts+tv < tv:
                    continue
                if s-tv+ts < ts:
                    continue
                if k-tv-ts > c-ts-1:
                    continue
                if c-ts-1 < 0:
                    continue
                if s-tv < 0:
                    continue
                if n-c-s+ts+tv < 0:
                    continue
                if k - tv-ts < 0:
                    continue
                if reqss-tv < 0:
                    continue
                if reqsc+1-ts < 0:
                    continue

                if reqsc + 1 - ts > 0:  # no requests can't progress
                    resc += math.comb(n-c-s+tv, tv) * math.comb(s-tv+ts, ts) * \
                        math.comb(c-ts-1, k-tv-ts) * Pcreqs(c-ts,
                                                            s-tv+ts, reqsc+1-ts, reqss-tv)

        # total probability (conditionnal probability)

        ans = (resc+ress) / (math.comb(n-1, k))

        array[c][s][reqsc][reqss] = ans
        if ans > 1.01:
            print(resc, ress, math.comb(n-1, k))
            sys.exit("Proba > 1.01 : " +
                     " ".join([str(c), str(s), str(reqsc), str(reqss)]))

        # print(
        #     "P(" + " ".join([str(c), str(s), str(reqsc), str(reqss)]) + ") = " + str(ans))
        return ans

    noCons = 0
    for i in range(0, n+1):
        for j in range(0, n+1):
            if i+j != n:
                noCons += Pcreqs(i, j, 0, 0)
    return noCons


nodes = range(3, 26)
ks = range(2, 13)


def computeAll(n, ks):
    resn = []
    for k in ks:
        if n > k:
            resn.append(getNoConsensusProb(n, k))
        else:
            resn.append(0)
    return resn


results = Parallel(n_jobs=-1)(delayed(computeAll)(n, ks) for n in nodes)

X, Y = np.meshgrid(ks, nodes)

fig = plt.figure()

ax = plt.axes(projection="3d")
ax.contour3D(X, Y, results, 80, cmap="viridis")
ax.set_xlabel("k")
ax.set_ylabel("n")
ax.set_zlabel("epsilon")

plt.show()
