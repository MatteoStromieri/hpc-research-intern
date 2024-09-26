import networkx as nx
import math 
import numpy as np
from helpers import complete_multigraph

VAL = 0
SCHEDULE = 1
"""
Input:
    - K = (V,E) a multiclique built with Preprocessing.cliqueBuilder()
    - D = (d_1, d_2, ...) data distribution accross nodes 
"""
def computeThreshold(K,D):
    G_balanced, alpha_balanced, beta_balanced = computeBalancedGraph(K)
    D_balanced = sum(D) / len(D)
    schedule = computeOptimalScheduleBalancedClique(G_balanced, alpha_balanced, beta_balanced, D_balanced)
    return (schedule[0] -1 )(alpha_balanced + beta_balanced*D_balanced)

def computeBalancedGraph(K):
    alphas = (nx.get_edge_attributes(K, 'alpha')).values()
    alpha_balanced = sum(alphas) / len(alphas)
    betas = (nx.get_edge_attributes(K, 'beta')).values()
    beta_balanced = sum(betas) / len(betas)
    G_balanced = complete_multigraph(K.number_of_nodes(),1,[alpha_balanced,beta_balanced])
    return G_balanced, alpha_balanced, beta_balanced

def computeOptimalScheduleBalancedClique(G, alpha, beta, D):
    n = G.number_of_nodes()
    opt = np.zeros((n,int(np.ceil(np.log2(n)))), dtype=object)
    for r in range(1,n+1):
        opt[r-1,0] = ( (r-1)*(alpha + D / beta), [r] )
    for c in range(2,int(np.ceil(np.log2(n)))+1):
        for r in range(2**c,n+1):
            S = []
            for s in range(2, int(math.sqrt(r)) + 1):
                if r%s == 0:
                    S.append(s)
            r_min = S[0]
            val_min = (S[0] - 1)*(alpha + (D*r)/(S[0]*beta)) + opt[r//S[0]-1,c-2][VAL]
            for k in S:
                val = (k - 1)*(alpha + (D*r)/(k*beta)) + opt[r//k-1,c-2][VAL]
                if val < val_min:
                    val_min = val
                    r_min = k
            l = list(opt[r//r_min-1,c-2][SCHEDULE])
            l.append(r_min)
            opt[r-1,c-1] = (val_min, l)
    sched_min = opt[n-1,0][SCHEDULE]
    val_min = opt[n-1,0][VAL]
    for c in range(1,int(np.ceil(np.log2(n)))+1):
        if opt[n-1,c-1][VAL] < val_min:
            sched_min = opt[n-1,c-1][SCHEDULE]
    return sched_min