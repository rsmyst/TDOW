import networkx as nx
import time
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

def load_graph():
    """Load the Wikipedia graph from data files"""
    print("Loading graph data...")
    start_time = time.time()
    
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
    
    elapsed = time.time() - start_time
    print(f"Graph loaded in {elapsed:.2f} seconds")
    print(f"Graph has {len(G.nodes)} nodes and {len(G.edges)} edges")
    
    return G, nodes

def analyze_connected_components(G):
    """Analyze the connected components of the graph"""
    components = list(nx.connected_components(G))
    component_sizes = [len(comp) for comp in components]
    
    stats = {
        "num_components": len(components),
        "largest_component_size": max(component_sizes),
        "component_size_distribution": Counter(component_sizes)
    }
    
    print(f"Graph has {len(components)} connected components")
    print(f"Largest component has {max(component_sizes)} nodes")
    
    return stats, components

def sample_path_lengths(G, sample_size=1000, max_pairs=1000000):
    """Sample path lengths by randomly selecting node pairs"""
    print(f"Sampling {sample_size} path lengths...")
    start_time = time.time()
    
    path_lengths = []
    unreachable_count = 0
    
    # Get list of nodes
    nodes = list(G.nodes())
    n = len(nodes)
    
    # Calculate total possible pairs
    total_pairs = n * (n - 1) // 2
    pairs_to_check = min(max_pairs, total_pairs)
    
    # Sample random pairs
    sampled_pairs = 0
    attempts = 0
    max_attempts = pairs_to_check * 10  # Avoid infinite loop
    
    while sampled_pairs < sample_size and attempts < max_attempts:
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        
        if i != j:
            attempts += 1
            try:
                length = nx.shortest_path_length(G, source=nodes[i], target=nodes[j])
                path_lengths.append(length)
                sampled_pairs += 1
                if sampled_pairs % 100 == 0:
                    print(f"Processed {sampled_pairs} pairs...")
            except nx.NetworkXNoPath:
                unreachable_count += 1
    
    elapsed = time.time() - start_time
    print(f"Sampled {len(path_lengths)} path lengths in {elapsed:.2f} seconds")
    
    return path_lengths, unreachable_count

def calculate_path_length_distribution(G, largest_component):
    """Calculate the distribution of path lengths in the largest component"""
    print("Calculating path length distribution in largest component...")
    start_time = time.time()
    
    # Sample subset of nodes from largest component for calculation
    # (Full calculation would be too computationally expensive)
    sample_size = min(100, len(largest_component))
    sampled_nodes = random.sample(list(largest_component), sample_size)
    
    path_lengths = defaultdict(int)
    pair_count = 0
    
    # Calculate shortest paths between all sampled node pairs
    for i, source in enumerate(sampled_nodes):
        if i % 10 == 0:
            print(f"Processing node {i+1}/{sample_size}...")
        
        # Single-source shortest paths
        lengths = nx.single_source_shortest_path_length(G, source)
        
        for target, length in lengths.items():
            if target != source and target in sampled_nodes:
                path_lengths[length] += 1
                pair_count += 1
    
    # Convert to regular dict for JSON serialization
    distribution = {str(k): v for k, v in sorted(path_lengths.items())}
    
    elapsed = time.time() - start_time
    print(f"Calculated {pair_count} path lengths in {elapsed:.2f} seconds")
    
    return distribution

def calculate_diameter(G, largest_component, approx=True):
    """Calculate exact or approximate diameter of the largest component"""
    print("Calculating graph diameter (this may take a while)...")
    start_time = time.time()
    
    # Create subgraph of largest component
    largest_subgraph = G.subgraph(largest_component)
    
    if approx:
        # Use approximation algorithm for faster calculation
        diameter = nx.approximation.diameter(largest_subgraph)
    else:
        # Exact but much slower calculation
        try:
            diameter = nx.diameter(largest_subgraph)
        except Exception as e:
            print(f"Error calculating exact diameter: {e}")
            print("Falling back to approximation...")
            diameter = nx.approximation.diameter(largest_subgraph)
    
    elapsed = time.time() - start_time
    print(f"Diameter calculation completed in {elapsed:.2f} seconds")
    
    return diameter

def main():
    """Main function to calculate and save path statistics"""
    # Load graph
    G, nodes = load_graph()
    
    # Analyze connected components
    component_stats, components = analyze_connected_components(G)
    
    # Get largest connected component
    largest_component = max(components, key=len)
    
    # Sample path lengths
    path_lengths, unreachable_count = sample_path_lengths(G, sample_size=5000)
    
    # Calculate path length distribution
    path_distribution = calculate_path_length_distribution(G, largest_component)
    
    # Calculate approximate diameter
    diameter = calculate_diameter(G, largest_component)
    
    # Compile statistics
    statistics = {
        "graph_info": {
            "num_nodes": len(G.nodes),
            "num_edges": len(G.edges),
            "avg_degree": 2 * len(G.edges) / len(G.nodes)
        },
        "component_stats": component_stats,
        "path_stats": {
            "sampled_paths": len(path_lengths),
            "unreachable_pairs": unreachable_count,
            "avg_path_length": sum(path_lengths) / len(path_lengths) if path_lengths else 0,
            "max_path_length": max(path_lengths) if path_lengths else 0,
            "min_path_length": min(path_lengths) if path_lengths else 0,
            "path_length_distribution": Counter(path_lengths),
            "component_path_distribution": path_distribution,
            "approximate_diameter": diameter
        }
    }
    
    # Save results to JSON file
    output_dir = Path("../backend/static")
    output_dir.mkdir(exist_ok=True)
    
    with open(output_dir / "path_statistics.json", "w") as f:
        json.dump(statistics, f, indent=2)
    
    print(f"Statistics saved to {output_dir}/path_statistics.json")
    
    # Print summary
    print("\nPath Length Statistics Summary:")
    print(f"Average path length: {statistics['path_stats']['avg_path_length']:.2f}")
    print(f"Maximum path length: {statistics['path_stats']['max_path_length']}")
    print(f"Minimum path length: {statistics['path_stats']['min_path_length']}")
    print(f"Approximate graph diameter: {diameter}")

if __name__ == "__main__":
    main() 