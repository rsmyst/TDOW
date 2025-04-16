import unittest
import json
from server import app, nodes, G
import networkx as nx

class PathFinderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    def test_index_route(self):
        response = self.app.get('/')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'Wikipedia Path Finder API')
    
    def test_valid_path(self):
        # Pick two nodes that we know exist in the dataset
        source = nodes[0]
        destination = nodes[5]
        
        # Check if path exists in the graph
        path_exists = nx.has_path(G, 0, 5)
        self.assertTrue(path_exists, "No path exists between test nodes")
        
        # Test the API
        response = self.app.post('/find-path',
                               data=json.dumps({'source': source, 'destination': destination}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Check structure of response
        self.assertIn('path', data)
        self.assertIn('distance', data)
        
        # Check that path is valid
        self.assertIsInstance(data['path'], list)
        self.assertGreater(len(data['path']), 0)
        self.assertEqual(data['path'][0], source)
        self.assertEqual(data['path'][-1], destination)
        
        # Check distance calculation
        self.assertEqual(data['distance'], len(data['path']) - 1)
    
    def test_nonexistent_article(self):
        response = self.app.post('/find-path',
                               data=json.dumps({'source': 'NonexistentArticle123', 'destination': nodes[0]}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['detail'], 'Article not found')
    
    def test_no_path_found(self):
        # Create a mock test for no path scenario
        # Since we don't know for sure which nodes have no path between them,
        # we'll mock this by temporarily removing all edges from a node
        
        # Store original neighbors to restore later
        node_id = 0
        if len(list(G.neighbors(node_id))) > 0:
            neighbors = list(G.neighbors(node_id))
            
            # Temporarily remove all edges
            for neighbor in neighbors:
                G.remove_edge(node_id, neighbor)
                
            try:
                # Now test with a node that should have no path
                response = self.app.post('/find-path',
                                       data=json.dumps({'source': nodes[node_id], 'destination': nodes[10]}),
                                       content_type='application/json')
                
                self.assertEqual(response.status_code, 404)
                data = json.loads(response.data)
                self.assertEqual(data['detail'], 'No path found between articles')
            finally:
                # Restore edges
                for neighbor in neighbors:
                    G.add_edge(node_id, neighbor)

    def test_same_source_destination(self):
        # Test when source and destination are the same
        source = nodes[0]
        
        response = self.app.post('/find-path',
                               data=json.dumps({'source': source, 'destination': source}),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        # Path should just be the single node
        self.assertEqual(len(data['path']), 1)
        self.assertEqual(data['path'][0], source)
        
        # Distance should be 0
        self.assertEqual(data['distance'], 0)
    
    def test_shortest_path(self):
        # Find nodes with a known shortest path
        # For simplicity, we'll use nodes with direct connection
        
        # Find a node with at least one neighbor
        for node_id in range(min(10, len(nodes))):
            neighbors = list(G.neighbors(node_id))
            if neighbors:
                neighbor_id = neighbors[0]
                
                # Confirm direct path exists
                self.assertEqual(nx.shortest_path_length(G, node_id, neighbor_id), 1)
                
                # Test the API
                response = self.app.post('/find-path',
                                      data=json.dumps({'source': nodes[node_id], 'destination': nodes[neighbor_id]}),
                                      content_type='application/json')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                
                # Check that we get the direct path (length 2: source and destination)
                self.assertEqual(len(data['path']), 2)
                self.assertEqual(data['distance'], 1)
                break

if __name__ == '__main__':
    unittest.main() 