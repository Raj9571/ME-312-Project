import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def recreate_graph_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()

    G = nx.Graph()
    node_id_map = {}
    new_id = 0

    # First pass to collect node positions and assign new IDs
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            node_id = parts[0]
            try:
                x, y = float(parts[1]), float(parts[2])
                node_type = 'Hospital' if node_id.startswith('H') else 'Emergency'
                if node_id not in node_id_map:  # Ensure each node is only added once
                    node_id_map[node_id] = (new_id, node_type)
                    G.add_node(new_id, pos=(x, y), node_type=node_type)
                    new_id += 1
            except ValueError:
                continue  # Skip lines that cannot be processed

    # Second pass to add edges with new IDs
    for line in lines:
        parts = line.split()
        if len(parts) == 3:
            try:
                node1, node2, weight = parts[0], parts[1], float(parts[2])
                if node1 in node_id_map and node2 in node_id_map:
                    G.add_edge(node_id_map[node1][0], node_id_map[node2][0], weight=weight)
            except ValueError:
                continue  # Ignore non-numeric weights

    return G, node_id_map

def save_graph_to_file(G, filename, node_id_map):
    with open(filename, 'w') as file:
        file.write(f"{G.number_of_nodes()}\n")
        # Reverse map to find original IDs from new numeric IDs
        reverse_map = {v[0]: (k, v[1]) for k, v in node_id_map.items()}
        for node, data in sorted(G.nodes(data=True), key=lambda x: x[0]):
            original_id, node_type = reverse_map[node]
            x, y = data['pos']
            file.write(f"{node_type[0]}{node} {x} {y}\n")
        for u, v, data in G.edges(data=True):
            u_type = reverse_map[u][1][0]  # First character of node type
            v_type = reverse_map[v][1][0]
            weight = data['weight']
            file.write(f"{u_type}{u} {v_type}{v} {weight}\n")


def visualize_graph(G):
    pos = nx.get_node_attributes(G, 'pos')
    colors = ['green' if data['node_type'] == 'Hospital' else 'red' for _, data in G.nodes(data=True)]
    sizes = [30 if data['node_type'] == 'Hospital' else 20 for _, data in G.nodes(data=True)]

    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, node_color=colors, node_size=sizes, with_labels=False, edge_color='gray')
    plt.title('Graph Visualization')
    plt.show()



file_path = 'ujjain_map_data.txt'
G, node_id_map = recreate_graph_from_file(file_path)
visualize_graph(G)  # Assuming visualize_graph does not need node_id_map
save_file_path = 'new_Ujjain.txt'
save_graph_to_file(G, save_file_path, node_id_map)
print(f"Graph saved in custom format to {save_file_path}")
