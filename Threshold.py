import networkx as nx
import numpy as np

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
    schedule = computeOptimalSchedule(G_balanced, alpha_balanced, beta_balanced, D_balanced)
    return (schedule[0] -1 )(alpha_balanced + beta_balanced*D_balanced)

def computeBalancedGraph(K):
    alphas = nx.get_edge_attributes(K, 'alpha')
    alpha_balanced = sum(alphas) / len(alphas)
    betas = nx.get_edge_attributes(K, 'beta')
    beta_balanced = sum(betas) / len(betas)
    G_balanced = nx.complete_graph(K.number_of_nodes())
    return G_balanced, alpha_balanced, beta_balanced

def computeOptimalScheduleBalancedClique(G, alpha, beta, D):
    n = G.number_of_nodes()
    opt = np.zeros((n,np.ceiling(np.log2(n))))
    for r in range(1,n+1):
        opt[r,1] = ( (r-1)*(alpha + D / beta), [r] )
    for c in range(2,np.ceiling(np.log2(n) + 1)):
        for r in range(2**c,n+1):
            S = []
            for s in range(2, sqrt(r) + 1):
                if r%s == 0:
                    S.append(s)
            r_min = S[0]
            val_min = (S[0] - 1)*(alpha + (D*(r/S[0])/beta)) + opt[r/S[0],c-1][VAL]
            for k in S:
                val = (k - 1)*(alpha + (D*(r/k)/beta)) + opt[r/k,c-1][VAL]
                if val < val_min:
                    val_min = val
                    r_min = k
            opt[r,c] = (val_min, list(opt[r/r_min,c-1][SCHEDULE].append(r_min)))
    sched_min = opt[n,1][SCHEDULE]
    val_min = opt[n,1][VAL]
    for c in range(1,np.ceiling(np.log2(n) + 1)):
        if opt[n,c].val < val_min:
            sched_min = opt[n,c].sched
    return sched_min