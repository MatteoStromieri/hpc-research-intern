import Preprocessing, Threshold, helpers
import DoubleEndedQueue as DEQ

PATH = 0
EXEC_TIME = 1
SS,SH,HS,HH = (0,1,2,3)
"""
Input:
    - H HashTable(key = virtual-edge, value = real-path) computed by Preprocessing.cliqueBuilder(...) 
    - threshold
    - K = (V_k,E_k) virtual clique computed by Preprocessing.cliqueBuilder(...) 
    - G = (V,E) real topology
    - D = [d1, d2,...] data size for every compute node
"""
def computeRings(h, threshold, K, G, d):
    q = DEQ.DoubleEndedQueue() # this is a double ended priority queue 
    pd = dict() # key = virtual-path | value = data sizes
    rings = [] # this list will contain the "optimal" rings, it is the output 
    for v in K.nodes:
        q.insert(Path(v))
    while not q.isEmpty():
        while q.readMax() >= threshold:
            p = q.popMax()
            d_max = d[0]
            for i in K.nodes:
                d_max = max(d_max, d[i])
            min_cost = float('inf')
            # K.get_edge_data(p.source, p.head) is dict key -> edge_data
            # I only need the keys (edge key)
            edges = K.get_edge_data(p.source, p.head).keys() 
            for e in edges:
                if ringCost(h, K, G, d, p, e) < min_cost:
                    e_opt = e
            updateBandwidth(K,G,pd,e_opt,p)
            q.updatePriorities(K,G,d,d_max)
            p.closePath(e_opt)
            rings.append(p)
        p = q.getMin()
        for w in q.sorted_list:
            if w == p:
                continue
            else:
                min_cost = float('inf')
                for edges, i in zip([K.get_edge_data(p.source, w.source), K.get_edge_data(p.source, w.head), K.get_edge_data(p.head, w.source), K.get_edge_data(p.head, w.head)],[SS,SH,HS,HH]):
                    for e in edges:
                        we_cost = cost(h, K, G, d, p, e, w)
                        if we_cost < min_cost:
                            w_opt = w
                            e_opt = e
                            min_cost = we_cost
                            marker = i
        if min_cost >= threshold:
            min_ring_cost = float('inf')
            edges = K.get_edge_data(p.source, p.head).keys() # dict key -> edge_data
            for e in edges:
                ring_cost = ringCost(h, K, G, d, p, e)
                if ring_cost < min_ring_cost:
                    e_opt = e
                    min_ring_cost = ring_cost
            if min_ring_cost >= threshold and min_ring_cost <= min_cost:
                updateBandwidth(K,G,pd,e_opt,p)
                q.updatePriorities(K,G,d,d_max)
                p.closePath(e_opt)
                rings.append(p)
            else: # merge W and P
                q.remove(w)
                p.addEdge(w, e_opt, marker)
                updateBandwidth(K,G,pd,w,e_opt,p, marker)
                q.add(p)
                q.updatePriorities(K,G,d,d_max)
        return rings



                
    pass 


class Path:
    def __init__(self, source):
        self.path = [] # list of (u,v,key) tuples
        self.source = source
        self.head = source
        self.priority = 0
    
    # add an edge (u,v) to the path
    def mergePaths(self, path, key, marker):
        pass   
    def closePath(self, key):
        pass 