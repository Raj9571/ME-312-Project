import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

def recreate_graph_from_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Initialize an empty graph
    G = nx.Graph()
    
    
    n_nodes = int(lines[0])
    
   
    for i in range(1, n_nodes+1):
        line = lines[i].split()
        node_type = line[0]
        node_id = f"{node_type}{line[1]}"
        x, y = float(line[2]), float(line[3])
        G.add_node(node_id, pos=(x, y), node_type=node_type)
    
    # Extract edges information
    for line in lines[n_nodes+1:]:
        node1, node2, weight = line.split()
        G.add_edge(node1, node2, weight=float(weight))
    
    return G


def visualize_graph(G):
    
    colors = {'E': 'blue', 'H': 'green', 'A': 'red'}
    sizes = {'E': 100, 'H': 200, 'A': 300}
    node_colors = [colors[data['node_type']] for _, data in G.nodes(data=True)]
    node_sizes = [sizes[data['node_type']] for _, data in G.nodes(data=True)]

   
    pos = nx.get_node_attributes(G, 'pos')

    
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=node_sizes, edge_color='gray', font_size=8)

  
    legend_handles = [mpatches.Patch(color=color, label=label) for label, color in colors.items()]
    plt.legend(handles=legend_handles, loc='best')

    plt.title('Visualized Graph from Text File')
    plt.axis('equal')  
    plt.show()

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def visualize_graph_with_path(G, path_edges):
    pos = nx.get_node_attributes(G, 'pos')
    # Define a color mapping
    color_map = {'E': 'blue', 'H': 'green', 'A': 'red'}
    # Apply the color mapping
    node_colors = [color_map[G.nodes[node]['node_type']] for node in G.nodes()]
    
    plt.figure(figsize=(12, 12))
    # Draw non-path edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, edge_color='lightgray', width=1, alpha=0.5)
    # Draw path edges
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    # Draw all nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=100)
    # Draw node labels
    nx.draw_networkx_labels(G, pos)

    plt.axis('off')
    plt.show()

# Use the code to recreate the graph G and the shortest path edges
# Then call the function with the graph and the shortest path edges
# visualize_graph_with_path(G, shortest_path_lp)


# Assuming `G` is your graph and `shortest_path_edges` is the list of edges obtained from the linear programming solution
# visualize_graph_with_path(G, shortest_path_edges)

# File path to the 'graph_structure.txt' file
file_path = 'graph_structure.txt'


G_recreated = recreate_graph_from_file(file_path)

#visualize_graph(G_recreated)
