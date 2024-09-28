import networkx as nx
from itertools import combinations

test_edges = {frozenset({1, 2}): {0: ([(2, 1, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.1, 'beta': 0.1})}, frozenset({1, 4}): {0: ([(4, 3, {'alpha': 0.1, 'beta': 0.1}), (3, 2, {'alpha': 0.5, 'beta': 0.1}), (2, 1, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.7, 'beta': 0.1}), 1: ([(4, 3, {'alpha': 0.1, 'beta': 0.1}), (3, 2, {'alpha': 0.1, 'beta': 0.1}), (2, 1, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.3, 'beta': 0.1})}, frozenset({2, 4}): {0: ([(4, 3, {'alpha': 0.1, 'beta': 0.1}), (3, 2, {'alpha': 0.5, 'beta': 0.1})], {'alpha': 0.6, 'beta': 0.1}), 1: ([(4, 3, {'alpha': 0.1, 'beta': 0.1}), (3, 2, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.2, 'beta': 0.1})}}

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
