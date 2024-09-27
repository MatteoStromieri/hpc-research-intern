import networkx as nx
import numpy as np
import gravis as gv

# n: number of nodes
# p: p(there are no edges between two nodes)
def generateMultiGraph(n, p):
    G = nx.MultiGraph()
    
    for i in range(n):
        G.add_node(i, weight_size=np.random.randint(min_size, max_size))

    for i in range(n):
        for j in range(i+1, n):
            for _ in range(np.random.geometric(p)-1):
                G.add_edge(i, j,  weight_gbps=np.random.randint(min_bandwidth, max_bandwidth), weight_latency=np.random.randint(min_latency, max_latency))       
    
    return G

def computeBalancedThreshold(G):
    pass
"""
def visualizeGraph(g):
    # Properties across the whole graph
    g.graph["node_color"] = "skyblue"
    g.graph["edge_color"] = "gray"
    g.graph["node_size"] = 30
    g.graph["node_label_size"] = 20
    
    # Properties for individual elements
    pos = nx.spring_layout(g)
    scaling_factor = 300
    for node, (x, y) in pos.items():
        g.nodes[node]["x"] = x * scaling_factor
        g.nodes[node]["y"] = y * scaling_factor
    return gv.d3(g, edge_curvature=0.1)
""" 

if __name__ == "__main__":
    # assuming a bandwidth between 1Gbps and 100Gbps
    min_bandwidth = 1
    max_bandwidth = 100
    # assuming a satum of size between 10 MB and 100 MB
    min_size = 10
    max_size = 100
    #
    min_latency = 1
    max_latency = 1
    #
    n_nodes = 5
    p = 1/2
    G = generateMultiGraph(n_nodes,p)
