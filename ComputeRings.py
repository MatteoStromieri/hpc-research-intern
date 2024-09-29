import Preprocessing, Threshold, helpers
import DoubleEndedQueue as DEQ
from MaxHeap import MaxHeap

MAX_SIZE = 2000
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
    ed = dict() # key = real-edge | value = sum of data that goes throught this edge at the same moment
    rings = [] # this list will contain the "optimal" rings, it is the output 
    for v in K.nodes:
        q.insert(Path(v, d[v]))
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
            updatePriorities(q,K,G,d,d_max)
            p.closePath(e_opt, ed)
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
    


def updatePriorities(q,K,G,d,d_max):
    pass
"""
Execution time of the path that we get if we merge p and w via edge e
"""
def cost(h, K, G, d, p, e, w):
    pass

def computePriority():
    pass
"""
Execution time of closed path
"""
def ringCost(h, d, p, e):
    pass

class Path:
    def __init__(self, source, data):
        self.path = [] # list of (u,v,key) tuples
        self.real_edges = dict() # real edge (u,v,k) -> times this path is passed throught this real edge
        self.most_trafficked_edge = 0 # the highest amount of data that passes throught the same physiscal edge
        self.most_trafficked_edge_data = list()
        self.in_path_data = MaxHeap(MAX_SIZE)
        self.in_path_data.insert(data)
        self.source = source
        self.head = source
        self.priority = 0
    
    # add an edge (u,v) to the path
    def mergePaths(self,h, ed, path, key, marker):
        for e in self.real_edges.keys():
            ed[e] -= sum(self.most_trafficked_edge_data[:self.real_edges[e]])
        for e in path.real_edges.keys():
            ed[e] -= sum(path.most_trafficked_edge_data[:path.real_edges[e]])            
        # 1st: update the list of edges
        if marker == SS:
            self.updateRealEdges(h, self.source, path.source, key)
            path.path.insert(0,(self.source, path.source, key))
            for edge in path.path:
                self.path.insert(0,(edge[1], edge[0], edge[2]))
            self.source = edge[1]
        elif marker == SH:
            self.updateRealEdges(h, self.source, path.head, key)
            self.path.insert(0,(path.head, self.source, key))
            self.path = path.path + self.path
            self.source = path.source
        elif marker == HS:
            self.updateRealEdges(h, self.head, path.source, key)
            self.path.append(0,(self.head, path.source, key))
            self.path = self.path + path.path
            self.head = path.head
        elif marker == HH:
            self.updateRealEdges(h, self.head, path.head, key)
            self.path.append(self.head, path.head, key)
            for edge in reversed(path.path):
                self.path.append((edge[1], edge[0], edge[2]))
            self.head = path.source
        # 2nd: update other data structures
        # merge dictionary of real_edges into self.real_edges
        self.most_trafficked_edge = helpers.mergeDictionaries(self.real_edges, path.real_edges, max(self.most_trafficked_edge, path.most_trafficked_edge))
        # now we have the maximum amount of data that goes throught the same real edge (k), therefore we
        # - merge the heaps
        # - extract the k highest values
        self.in_path_data.merge(path.in_path_data)
        data = self.most_trafficked_edge_data + path.most_trafficked_edge_data
        for d in data:
            self.in_path_data.insert(d)
        self.most_trafficked_edge_data = []
        i = 0
        while i < self.most_trafficked_edge:
            self.most_trafficked_edge_data.append(self.in_path_data.extractMax())
        # now update the ed dictionary with new values
        for e in self.real_edges.keys():
            ed[e] = ed.setdefault(e,0) + sum(self.most_trafficked_edge_data[:self.real_edges[e]])

    def updateRealEdges(self, h, head, source, key):
        r_edges = h[frozenset([head, source])][key][0] # r_edges = [(u,v,k1,{alpha, beta}), (v,w,k2,{alpha,beta}), ...]
        for r_e in r_edges:
            index = helpers.edHash(r_e)
            self.real_edges[index] = self.real_edges.setdefault(index,0) + 1
            if self.real_edges[index] > self.most_trafficked_edge:
                self.most_trafficked_edge += 1
                self.most_trafficked_edge_data.append(self.in_path_data.extractMax())
    
    def closePath(self, h, ed, key):
        self.path.append((self.head, self.source, key))
        self.head = self.source
        r_edges = h[frozenset([self.head, self.source])][key][0]
        for r_e in r_edges:
            index = helpers.edHash(r_e)
            self.real_edges[index] += 1
            if self.real_edges[index] > self.most_trafficked_edge:
                self.most_trafficked_edge += 1
                self.most_trafficked_edge_data.append(self.in_path_data.extractMax())
            ed[index] = ed.setdefault(index,0) + self.most_trafficked_edge_data[self.real_edges[index]]
    