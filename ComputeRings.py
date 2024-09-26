import Preprocessing, Threshold, helpers
import DoubleEndedQueue


"""
Input:
    - H HashTable(key = virtual-edge, value = real-path) computed by Preprocessing.cliqueBuilder(...) 
    - K = (V_k,E_k) virtual clique computed by Preprocessing.cliqueBuilder(...) 
    - G = (V,E) real topology
    - D = [d1, d2,...] data size for every compute node
"""
def ComputeRings(h, K, G, d):
    q = DEPQ() # this is a double ended priority queue (https://github.com/ofek/depq)
    pd = dict() # key = virtual-path | value = data sizes
    rings = [] # this list will contain the "optimal" rings, it is the output 
    for v in K.nodes():
        q.insert()