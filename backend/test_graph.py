import unittest
import networkx as nx
from server import G, nodes

class GraphTestCase(unittest.TestCase):
    def test_graph_loaded(self):
        """Test that the graph was loaded with data"""
        self.assertGreater(len(G.nodes), 0, "Graph has no nodes")
        self.assertGreater(len(G.edges), 0, "Graph has no edges")
        self.assertGreaterEqual(len(nodes), len(G.nodes), "Node list doesn't match graph nodes")
    
    def test_node_properties(self):
        """Test that node properties are correctly set"""
        for i in range(min(10, len(nodes))):
            self.assertIn(i, G.nodes)
            self.assertEqual(G.nodes[i].get('title'), nodes[i])
    
    def test_direct_path_finding(self):
        """Test path finding directly using NetworkX"""
        # Find a node with at least one neighbor
        for node_id in range(min(10, len(nodes))):
            neighbors = list(G.neighbors(node_id))
            if neighbors:
                neighbor_id = neighbors[0]
                
                # Test direct shortest path
                path = nx.shortest_path(G, node_id, neighbor_id)
                self.assertEqual(len(path), 2)
                self.assertEqual(path[0], node_id)
                self.assertEqual(path[1], neighbor_id)
                
                # Test distance
                distance = nx.shortest_path_length(G, node_id, neighbor_id)
                self.assertEqual(distance, 1)
                break
    
    def test_indirect_path_finding(self):
        """Test finding a path that requires multiple hops"""
        # This test is more complex as we need to find nodes with a known
        # path of length > 1, without modifying the graph
        
        # Try to find a path with length at least 2
        found_path = False
        for start_node in range(min(5, len(nodes))):
            for end_node in range(min(10, len(nodes))):
                if start_node == end_node:
                    continue
                    
                if nx.has_path(G, start_node, end_node):
                    path_length = nx.shortest_path_length(G, start_node, end_node)
                    if path_length >= 2:
                        # Found a path with at least one intermediate node
                        path = nx.shortest_path(G, start_node, end_node)
                        
                        # Verify path properties
                        self.assertEqual(len(path), path_length + 1)
                        self.assertEqual(path[0], start_node)
                        self.assertEqual(path[-1], end_node)
                        
                        # Convert indices to titles
                        path_titles = [nodes[i] for i in path]
                        self.assertEqual(path_titles[0], nodes[start_node])
                        self.assertEqual(path_titles[-1], nodes[end_node])
                        
                        found_path = True
                        break
            
            if found_path:
                break
                
        self.assertTrue(found_path, "Could not find a multi-hop path in the graph")
    
    def test_graph_connectivity(self):
        """Test overall graph connectivity"""
        # Get the largest connected component
        largest_cc = max(nx.connected_components(G), key=len)
        
        # Print some statistics for debugging
        print(f"Graph has {len(G.nodes)} nodes and {len(G.edges)} edges")
        print(f"Largest connected component has {len(largest_cc)} nodes")
        
        # Test connectivity between random nodes in the largest component
        if len(largest_cc) >= 2:
            nodes_in_cc = list(largest_cc)
            start_node = nodes_in_cc[0]
            end_node = nodes_in_cc[-1]
            
            # There should be a path between these nodes
            self.assertTrue(nx.has_path(G, start_node, end_node))

if __name__ == '__main__':
    unittest.main() 