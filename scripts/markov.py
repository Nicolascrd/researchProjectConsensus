import math
import numpy as np
from joblib import Parallel, delayed
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def getNoConsensusProb(n, k):

    array = np.ndarray(shape=(n+1, n+1), dtype=float)
    array.fill(-1)  # table contains -1 if the probability was not yet computed
    for i in range(n+1):
        array[0][i] = 0

    # one node receives the information and emits one group of requests
    array[1][1] = 1

    def Pcreqs(c, reqs):
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

            if reqs + 1 - t > 0:  # no requests can't progress
                res += math.comb(n-c+t, t) * math.comb(c-t-1, k-t) * \
                    Pcreqs(c-t, reqs+1-t)
        ans = res / math.comb(n-1, k)
        array[c][reqs] = ans
        return ans
    noCons = 0
    for i in range(0, n+1):
        if i != n:
            noCons += Pcreqs(i, 0)
    return noCons


nodes = range(3, 26)
ks = range(2, 13)


def computeAll(n, ks):
    resn = []
    for k in ks:
        if n > k:
            g = getNoConsensusProb(n, k)
            if g == 0:
                resn.append(0)
            else:
                resn.append(getNoConsensusProb(n, k))
        else:
            resn.append(0)
    return resn


results = Parallel(n_jobs=-1)(delayed(computeAll)(n, ks) for n in nodes)

X, Y = np.meshgrid(ks, nodes)

fig = plt.figure()

ax = plt.axes(projection="3d")
ax.contour3D(X, Y, results, 200, cmap="viridis")
ax.set_xlabel("k")
ax.set_ylabel("n")
ax.set_zlabel("epsilon")
ax.set_title("Probability of not reaching consensus")
plt.show()
