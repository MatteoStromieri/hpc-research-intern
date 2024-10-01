import networkx as nx
import matplotlib.pyplot as plt

"""
Input: 
- Topology Graph G : each node is a "compute node" (C) or a "switch"(S), each edge has a weight (alpha, beta)
"""
SWITCH = "S"
COMPUTE_NODE = "C"

def cliqueBuilder(G):
    compute_nodes = getComputeNodes(G)
    # create a graph without adges and with V\S as vertices
    G_clique = nx.MultiGraph()
    G_clique.add_nodes_from(compute_nodes)
    # dictionary: virtual edge -> path
    vedge_to_paths = dict()
    # find all paths for each couple of nodes
    for u in compute_nodes:
        for v in compute_nodes:
            nodes = frozenset([u,v])
            if u <= v or nodes in vedge_to_paths.keys():
                continue
            # findAllPaths returns a list of paths, a path is a list of edges coupled with a dict that contains two values (alpha -> float, beta -> float)
            paths = findAllPaths(G,u,v, [], [], [], 0, float('inf'))
            vedge_to_paths[nodes] = dict()
            k = 0
            for path in paths:
                vedge_to_paths[nodes][k] = path
                G_clique.add_edge(u,v)
                G_clique.edges[u,v,k].update(path[1])
                k += 1
    return G_clique, vedge_to_paths
"""
Input:
- Topology G
- {u,v} a set of two nodes: u is the source, v is the target
Output:
- A list of paths [p1,p2,...]

Each path pi is given by a couple ([e1,e2,...],(alpha -> float, beta -> float))
"""
def findAllPaths(G, u, v, connectionPaths = list(), connectionPath = list(), connectionPathNodes = list(), alpha = 0, beta = float('inf')):
    connectionPathNodes.append(u)
    for edge in G.edges(u, data = True, keys = True):
        (u,x,k,d) = edge
        if x == v:
            connectionPath.append(edge)
            alpha += d['alpha']
            prev_beta = beta
            beta = min(beta, d['beta'])
            temp = list(connectionPath)
            connectionPaths.append((temp,{'alpha':round(alpha,1), 'beta':beta}))
            connectionPath.pop()
            alpha -= d['alpha']
            beta = prev_beta
        elif x not in connectionPathNodes:
            alpha += d['alpha']
            prev_beta = beta
            beta = min(beta, d['beta'])
            connectionPath.append(edge)
            findAllPaths(G, x, v, connectionPaths, connectionPath, connectionPathNodes, alpha, beta)
            connectionPath.pop()
            alpha -= d['alpha']
            beta = prev_beta
    connectionPathNodes.pop()
    return connectionPaths





def getComputeNodes(G):
    return [n for n, attrs in G.nodes(data=True) if attrs.get('node_type') == COMPUTE_NODE]

