import Preprocessing, Threshold, helpers
import DoubleEndedQueue as DEQ
from MaxHeap import MaxHeap
import copy
import networkx as nx
import json

MAX_SIZE = 2000
PATH = 0
EXEC_TIME = 1
SS,SH,HS,HH = (0,1,2,3)
NODE1, NODE2, KEY = (0,1,2)
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
        q.insert(Path(v, d[v]),G, K, h, ed)
    print(f"queue: {q.sorted_list}")
    while not q.isEmpty():
        print(q.toString())
        while q.readMax().getExecTime(G, K, h, ed) >= threshold:
            p = q.popMax()
            d_max = d[0]
            for i in K.nodes:
                d_max = max(d_max, d[i])
            min_cost = float('inf')
            # K.get_edge_data(p.source, p.head) is dict key -> edge_data
            # I only need the keys (edge key)
            key,_ = p.getBestClosure(G,K,h,ed)
            p.closePath(h, ed, key)
            updatePriorities(q,K,G,d,d_max)
            rings.append(p)
            if q.isEmpty():
                break
        if q.isEmpty():
            break
        p = q.getMin()
        for w in q.sorted_list:
            if w == p:
                continue
            else:
                min_cost = float('inf')
                for edges, i in zip([K.get_edge_data(p.source, w.source).keys(), K.get_edge_data(p.source, w.head).keys(), K.get_edge_data(p.head, w.source).keys(), K.get_edge_data(p.head, w.head).keys()],[SS,SH,HS,HH]):
                    for e in edges:
                        we_cost = cost(h, ed, K, G, d, p, e, w, i)
                        if we_cost < min_cost:
                            w_opt = w
                            e_opt = e
                            min_cost = we_cost
                            marker = i
        print(f"min_cost = {min_cost} | e_opt = {e_opt} | w_opt = {w_opt.toString()} | path_p = {p.path} - edge = {p.source, w_opt.source} - path_w = {w_opt.path} | moved_data = {sum(ed.values())} ")
        if min_cost >= threshold:
            if p.isClosed():
                min_key, min_ring_cost = (None,float('inf'))    
            else:
                min_key, min_ring_cost = p.getBestClosure(G,K,h,ed)
                print(f"min_key = {min_key} | min_ring_cost = {min_ring_cost}")
            if min_ring_cost >= threshold and min_ring_cost <= min_cost:
                p.closePath(h, ed, min_key)
                q.reset(G,K,h,ed)
                rings.append(p)
            else: # merge W and P
                q.remove(w_opt)
                p.mergePaths(h, ed, w_opt, e_opt, marker)
                q.insert(p,G,K,h,ed)
                q.reset(G,K,h,ed)
    return rings
    


def updatePriorities(q,K,G,h,ed):
    q.reset( G, K, h, ed)

"""
Execution time of the path that we get if we merge p and w via edge e
"""
def cost(h, ed, K, G, d, p, e_key, w, marker):
    p_dup = p.duplicate()
    w_dup = w.duplicate()
    ed_dup = copy.copy(ed)
    h_dup = copy.copy(h)
    p_dup.mergePaths(h_dup,ed_dup,w_dup,e_key,marker)
    t = p_dup.getExecTime(G, K, h_dup, ed_dup)
    print(f"moved_data = {ed_dup} | time = {t}")
    return t

"""
Execution time of closed path
"""
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
    
    def toRealRing(self,h):
        real_ring = []
        for v_e in self.path:
            real_ring.append(h[frozenset([v_e[0],v_e[1]])][v_e[2]])
        return real_ring
    
    def toString(self):
        return ''.join(str(e) for e in self.path)
    
    # add an edge (u,v) to the path
    def mergePaths(self,h, ed, path, key, marker):
        for e in self.real_edges.keys():
            ed[e] -= sum(self.most_trafficked_edge_data[:self.real_edges[e]])
        for e in path.real_edges.keys():
            ed[e] -= sum(path.most_trafficked_edge_data[:path.real_edges[e]])            
        # 1st: update the list of edges
        if marker == SS:
            self.updateRealEdgesWithoutEd(h, self.source, path.source, key)
            path.path.insert(0,(self.source, path.source, key))
            for edge in path.path:
                self.path.insert(0,(edge[1], edge[0], edge[2]))
            self.source = edge[1]
        elif marker == SH:
            self.updateRealEdgesWithoutEd( h, self.source, path.head, key)
            self.path.insert(0,(path.head, self.source, key))
            self.path = path.path + self.path
            self.source = path.source
        elif marker == HS:
            self.updateRealEdgesWithoutEd(h, self.head, path.source, key)
            self.path.append((self.head, path.source, key))
            self.path = self.path + path.path
            self.head = path.head
        elif marker == HH:
            self.updateRealEdgesWithoutEd(h, self.head, path.head, key)
            self.path.append((self.head, path.head, key))
            for edge in reversed(path.path):
                self.path.append((edge[1], edge[0], edge[2]))
            self.head = path.source
        # 2nd: update other data structures
        # merge dictionary of real_edges into self.real_edges
        self.most_trafficked_edge = helpers.mergeDictionaries(self.real_edges, path.real_edges, self.most_trafficked_edge)
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
            i += 1
        # now update the ed dictionary with new values
        for e in self.real_edges.keys():
            ed[e] = ed.setdefault(e,0) + sum(self.most_trafficked_edge_data[:self.real_edges[e]])

    def updateRealEdges(self, ed, h, head, source, key):
        r_edges = h[frozenset([head, source])][key][0] # r_edges = [(u,v,k1,{alpha, beta}), (v,w,k2,{alpha,beta}), ...]
        for r_e in r_edges:
            index = helpers.edHash(r_e)
            self.real_edges[index] = self.real_edges.setdefault(index,0) + 1
            if self.real_edges[index] > self.most_trafficked_edge:
                self.most_trafficked_edge += 1
                self.most_trafficked_edge_data.append(self.in_path_data.extractMax())
            ed[index] = ed.setdefault(index,0) + self.most_trafficked_edge_data[self.real_edges[index] - 1]
            
    def updateRealEdgesWithoutEd(self, h, head, source, key):
        r_edges = h[frozenset([head, source])][key][0] # r_edges = [(u,v,k1,{alpha, beta}), (v,w,k2,{alpha,beta}), ...]
        for r_e in r_edges:
            index = helpers.edHash(r_e)
            self.real_edges[index] = self.real_edges.setdefault(index,0) + 1
            if self.real_edges[index] > self.most_trafficked_edge:
                self.most_trafficked_edge += 1
                self.most_trafficked_edge_data.append(self.in_path_data.extractMax())
            
    
    def closePath(self, h, ed, key):
        self.path.append((self.head, self.source, key))
        r_edges = h[frozenset([self.head, self.source])][key][0]
        self.head = self.source
        for r_e in r_edges:
            index = helpers.edHash(r_e)
            self.real_edges[index] = self.real_edges.setdefault(index,0) + 1
            if self.real_edges[index] > self.most_trafficked_edge:
                self.most_trafficked_edge += 1
                self.most_trafficked_edge_data.append(self.in_path_data.extractMax())
            ed[index] = ed.setdefault(index,0) + self.most_trafficked_edge_data[self.real_edges[index] - 1]

    def isClosed(self):
        return self.source == self.head
    
    def duplicate(self):
        self_new = Path(None,0)
        self_new.real_edges = copy.copy(self.real_edges)
        self_new.most_trafficked_edge = self.most_trafficked_edge
        self_new.most_trafficked_edge_data = copy.copy(self.most_trafficked_edge_data)
        self_new.in_path_data = self.in_path_data.duplicate()
        self_new.source = self.source
        self_new.head = self.head
        return self_new

    def getBestClosure(self,G,K,h,ed):
        keys = K.get_edge_data(self.source, self.head).keys()
        k_opt = None
        t_opt = float('inf')
        for key in keys:
            self_copy = self.duplicate()
            h_copy = copy.copy(h)
            ed_copy = copy.copy(ed)
            self_copy.closePath(h_copy, ed_copy, key)
            t = self_copy.getExecTime(G,K,h_copy,ed_copy)
            if t < t_opt:
                k_opt = key
                t_opt = t
        return k_opt, t_opt

    def getExecTime(self, G, K, h, ed):
        exec_time = 0
        if self.isClosed():
            exec_time = 0
            for r_e in self.real_edges.keys():
                r_e_alpha, r_e_beta = G.get_edge_data(r_e[NODE1],r_e[NODE2],r_e[KEY]).values()
                t_e = ed[r_e] / r_e_beta
                exec_time += r_e_alpha*self.real_edges[r_e] + t_e*self.real_edges[r_e]
            return exec_time
        else:
            _, exec_time = self.getBestClosure(G,K,h,ed) 
            return exec_time

if __name__ == '__main__':
    # define graph topology
    G = helpers.getBalancedFatTree(0.1,1)
    # build clique
    G_clique, h = Preprocessing.cliqueBuilder(G)
    #get threshold
    data = {0:100000000000000,1:100000000000000,3:100000000000000,4:100000000000000}
    threshold = Threshold.computeThreshold(G_clique, data)
    print(f"The threshold for G has been computed: {threshold}")
    # compute rings
    rings = computeRings(h, threshold, G_clique, G, data)
    print("Now I print the rings")
    for r,i in zip(rings,range(len(rings))):
        print(f"Ring {i} -> {''.join(str(tup) for tup in r.toRealRing(h))}")
