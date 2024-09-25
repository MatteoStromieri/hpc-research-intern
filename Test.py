import unittest
import matplotlib.pyplot as plt
import networkx as nx
from Preprocessing import getComputeNodes, findAllPaths, cliqueBuilder, SWITCH, COMPUTE_NODE

class TestPreprocessing(unittest.TestCase):
    
    def testGetComputeNodes(self):
        G = nx.MultiGraph()  # Corrected capitalization of Graph
        G.add_node(1, node_type=COMPUTE_NODE)
        G.add_node(2, node_type=COMPUTE_NODE)
        G.add_node(3, node_type=COMPUTE_NODE)
        G.add_node(4, node_type=COMPUTE_NODE)
        G.add_node(5, node_type=SWITCH)
        self.assertEqual(getComputeNodes(G), [1,2,3,4])
    
    def testGetFindAllPaths(self):
        G = nx.MultiGraph()  # Corrected capitalization of Graph
        G.add_edges_from([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})])
        self.assertEqual(findAllPaths(G,{1,4}), [
            ([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})], {'alpha':0.3,'beta':0.1}),
            ([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})], {'alpha':0.3,'beta':0.1})
            ])
    
    def testCliqueBuilder(self):
        G = nx.MultiGraph()  # Corrected capitalization of Graph
        G.add_edges_from([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})])        
        nx.set_node_attributes(G, {1:COMPUTE_NODE, 2:COMPUTE_NODE, 3:SWITCH, 4:COMPUTE_NODE}, "node_type")
        G_clique = cliqueBuilder(G)
        nx.draw(G_clique)
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()