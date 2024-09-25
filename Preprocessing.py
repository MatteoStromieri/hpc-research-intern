import networkx as nx
import pprint 
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
    vedge_to_path = dict()
    # find all paths for each couple of nodes
    for u in compute_nodes:
        for v in compute_nodes:
            nodes = frozenset([u,v])
            if u <= v or nodes in vedge_to_path.keys():
                continue
            # findAllPaths returns a list of paths, a path is a list of edges coupled with a dict that contains two values (alpha -> float, beta -> float)
            paths = findAllPaths(G,u,v, [], [], [], 0, float('inf'))
            print(f"Paths found between {u} and {v}: \n {paths} \n ------------------------------------")
            vedge_to_path[nodes] = list()
            k = 0
            for path in paths:
                vedge_to_path[nodes].append(path)
                G_clique.add_edge(u,v)
                G_clique.edges[u,v,k].update(path[1])
                k += 1
    pprint.pprint(nx.get_edge_attributes(G_clique, 'beta'))
    #pprint.pprint(vedge_to_path)
    return G_clique
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
    for edge in G.edges(u, data = True):
        (u,x,d) = edge
        #print(f"({u},{x})")
        if x == v:
            connectionPath.append(edge)
            alpha += d['alpha']
            prev_beta = beta
            beta = min(beta, d['beta'])
            temp = list(connectionPath)
            connectionPaths.append((temp,{'alpha':round(alpha,1), 'beta':beta}))
            #print(f"Path found: {temp} with attributes {{'alpha': {alpha}, 'beta': {beta}}}")
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

"""
Main function for test purposes
"""

if __name__ == '__main__':
    G = nx.MultiGraph()  # Corrected capitalization of Graph
    G.add_edges_from([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.5, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})])        
    nx.set_node_attributes(G, {1:COMPUTE_NODE, 2:COMPUTE_NODE, 3:SWITCH, 4:COMPUTE_NODE}, "node_type")
    print("Paths between 2 and 1")
    #pprint.pprint(findAllPaths(G, 2, 1))
    print("Paths between 4 and 2")
    pprint.pprint(findAllPaths(G, 4, 2, [], [], [], 0, float('inf')))
    print("Paths between 4 and 1")
    pprint.pprint(findAllPaths(G, 4, 1, [], [], [], 0, float('inf')))
    print("------------------------------------------------------")
    cliqueBuilder(G)
    """
    G_clique = cliqueBuilder(G)
    nx.draw(G_clique)
    plt.show()
    """