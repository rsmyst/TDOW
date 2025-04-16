from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import networkx as nx
import os

app = Flask(__name__)
CORS(app)

# Load graph data
def load_graph():
    G = nx.Graph()
    
    # Load nodes
    with open("../data/nodes.txt", "r", encoding="utf-8") as f:
        nodes = [line.strip() for line in f]
    
    # Add nodes to graph
    for i, node in enumerate(nodes):
        G.add_node(i, title=node)
    
    # Load edges
    with open("../data/edges.txt", "r", encoding="utf-8") as f:
        for line in f:
            source, target = map(int, line.strip().split())
            G.add_edge(source, target)
    
    return G, nodes

# Initialize graph
G, nodes = load_graph()

@app.route('/')
def index():
    return jsonify({"message": "Wikipedia Path Finder API"})

@app.route('/suggest', methods=['GET'])
def suggest_articles():
    query = request.args.get('q', '').lower()
    if not query or len(query) < 2:
        return jsonify([])
    
    # Find matching articles (case insensitive)
    suggestions = [node for node in nodes if query in node.lower()]
    # Limit results to avoid overwhelming the client
    return jsonify(suggestions[:10])

@app.route('/find-path', methods=['POST'])
def find_path():
    data = request.json
    source = data.get('source')
    destination = data.get('destination')
    
    try:
        # Find node indices
        source_idx = nodes.index(source)
        target_idx = nodes.index(destination)
        
        # Find shortest path
        path = nx.shortest_path(G, source=source_idx, target=target_idx)
        
        # Convert indices to titles
        path_titles = [nodes[i] for i in path]
        
        return jsonify({
            "path": path_titles,
            "distance": len(path) - 1
        })
    except ValueError:
        return jsonify({"detail": "Article not found"}), 404
    except nx.NetworkXNoPath:
        return jsonify({"detail": "No path found between articles"}), 404

@app.route('/path-statistics', methods=['GET'])
def get_path_statistics():
    static_dir = os.path.join(os.path.dirname(__file__), 'static')
    try:
        return send_from_directory(static_dir, 'path_statistics.json')
    except FileNotFoundError:
        return jsonify({"detail": "Statistics not available. Run path_statistics.py first."}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True) 