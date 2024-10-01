import networkx as nx
from itertools import combinations
from Preprocessing import COMPUTE_NODE, SWITCH

test_edges = {frozenset({1, 2}): {0: ([(2, 1, 0, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.1, 'beta': 0.1})}, 
              frozenset({1, 4}): {0: ([(4, 3, 0, {'alpha': 0.1, 'beta': 0.1}), (3, 2, 0, {'alpha': 0.5, 'beta': 0.1}), (2, 1, 0, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.7, 'beta': 0.1}), 1: ([(4, 3, 0, {'alpha': 0.1, 'beta': 0.1}), (3, 2, 1, {'alpha': 0.1, 'beta': 0.1}), (2, 1, 0, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.3, 'beta': 0.1})}, 
              frozenset({2, 4}): {0: ([(4, 3, 0, {'alpha': 0.1, 'beta': 0.1}), (3, 2, 0, {'alpha': 0.5, 'beta': 0.1})], {'alpha': 0.6, 'beta': 0.1}), 1: ([(4, 3, 0, {'alpha': 0.1, 'beta': 0.1}), (3, 2, 1, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.2, 'beta': 0.1})}}
def node_match(n1, n2):
    return n1['name'] == n2['name']

def edge_match(e1, e2):
    return e1.get('alpha') == e2.get('alpha') and e1.get('beta') == e2.get('beta') 

def complete_multigraph(n, num_edges_between_each_pair, weights):
    # Create an empty multigraph
    G = nx.MultiGraph()
    
    # Add nodes
    G.add_nodes_from(range(n))
    
    # Add multiple edges between every pair of nodes
    for u, v in combinations(range(n), 2):  # combinations will give all unique pairs
        for _ in range(num_edges_between_each_pair):
            G.add_edge(u, v, alpha = weights[0], beta = weights[1])
    
    return G

"""
Every input dictionary has an edge as key and an int as value, we want to sum the values related to the same key
"""
def mergeDictionaries(dict1, dict2, val):
    for key in dict2.keys():
        dict1[key] = dict1.setdefault(key,0) + dict2[key]
        if val < dict1[key]:
            val = dict1[key]
    return val

def edHash(r_edge, u=None, v=None):
    if u == None and v == None:
        return (min(r_edge[0],r_edge[1]), max(r_edge[0],r_edge[1]),r_edge[2])
    else:
        return (min(u,v), max(u,v), r_edge)

def getBalancedFatTree(alpha, beta):
    G = nx.MultiGraph()  # Corrected capitalization of Graph
    G.add_edges_from([(0,2,{'alpha':alpha, 'beta':beta}),(1,2,{'alpha':alpha, 'beta':beta}),(3,5,{'alpha':alpha, 'beta':beta}),(4,5,{'alpha':alpha, 'beta':beta}), (2,6,{'alpha':alpha, 'beta':beta}),(2,6,{'alpha':alpha, 'beta':beta}),(5,6,{'alpha':alpha, 'beta':beta}),(5,6,{'alpha':alpha, 'beta':beta})])
    nx.set_node_attributes(G, {0:COMPUTE_NODE, 1:COMPUTE_NODE, 2:SWITCH, 3:COMPUTE_NODE, 4:COMPUTE_NODE, 5:SWITCH, 6:SWITCH}, "node_type")
    return G
        


