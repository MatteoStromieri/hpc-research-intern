import unittest
import networkx as nx
from Preprocessing import getComputeNodes, findAllPaths, cliqueBuilder, SWITCH, COMPUTE_NODE
from Threshold import computeThreshold, computeBalancedGraph, computeOptimalScheduleBalancedClique
import helpers

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
        found_paths = findAllPaths(G,1,4)
        print(found_paths)
        self.assertEqual(found_paths, [([(1, 2, 0, {'alpha': 0.1, 'beta': 0.1}), (2, 3, 0, {'alpha': 0.1, 'beta': 0.1}), (3, 4, 0, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.3, 'beta': 0.1}), ([(1, 2, 0, {'alpha': 0.1, 'beta': 0.1}), (2, 3, 0, {'alpha': 0.1, 'beta': 0.1}), (3, 4, 1, {'alpha': 0.1, 'beta': 0.1})], {'alpha': 0.3, 'beta': 0.1})])

    def testCliqueBuilder(self):
        G = nx.MultiGraph()  # Corrected capitalization of Graph
        G.add_edges_from([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.5, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})])        
        nx.set_node_attributes(G, {1:COMPUTE_NODE, 2:COMPUTE_NODE, 3:SWITCH, 4:COMPUTE_NODE}, "node_type")
        _, edges = cliqueBuilder(G)
        print(edges)
        self.assertDictEqual(edges, helpers.test_edges)

    def testComputeBalancedGraph(self):
        G_clique = nx.MultiGraph()
        G_clique.add_edges_from([(1,2,{'alpha':0.1, 'beta':0.1}),(2,3,{'alpha':0.5, 'beta':0.1}),(2,3,{'alpha':0.1, 'beta':0.1}),(3,4,{'alpha':0.1, 'beta':0.1})])
        G_balanced, _, _ = computeBalancedGraph(G_clique)
        G_test = nx.MultiGraph()
        G_test.add_edges_from([(1,2,{'alpha':0.2, 'beta':0.1}),(1,3,{'alpha':0.2, 'beta':0.1}),(1,4,{'alpha':0.2, 'beta':0.1}), (2,3,{'alpha':0.2, 'beta':0.1}), (2,4,{'alpha':0.2, 'beta':0.1}), (3,4,{'alpha':0.2, 'beta':0.1})])
        self.assertTrue(nx.is_isomorphic(G_balanced, G_test, edge_match=helpers.edge_match))    

    def testComputeOptimalScheduleBalancedClique(self):
        alpha = 1
        beta = 1
        n = 4
        data = 1
        sched_expected = [2,2]
        G = helpers.complete_multigraph(n,1,[alpha, beta]) # alpha = 1 and beta = 1 for simplicity
        sched = computeOptimalScheduleBalancedClique(G, alpha, beta, data)
        self.assertEquals(sched, sched_expected)

    def testComputeRings(self):
        pass

if __name__ == '__main__':
    unittest.main()