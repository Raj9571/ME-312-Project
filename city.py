import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.patches as mpatches
from optimal_location import find_optimal_locations


def connect_components(G):
    
    components = list(nx.connected_components(G))
    largest_component = max(components, key=len)
    other_components = [comp for comp in components if comp != largest_component]
    
    # For each disconnected component, find the closest node in the largest component and connect them
    for component in other_components:
        min_distance = float('inf')
        closest_nodes = None
        for node_in_comp in component:
            for node_in_largest in largest_component:
                distance = np.linalg.norm(np.array(G.nodes[node_in_comp]['pos']) - np.array(G.nodes[node_in_largest]['pos']))
                if distance < min_distance:
                    min_distance = distance
                    closest_nodes = (node_in_comp, node_in_largest)
        # Add edge between the closest nodes of the disconnected component and the largest component
        if closest_nodes:
            G.add_edge(*closest_nodes, weight=min_distance)

np.random.seed(42)
n_emergency_calls = 200
n_hospitals = 10
max_connection_distance = 20  # Maximum distance for direct connection
connection_probability = 0.1  # Probability of connecting two nodes within max distance



emergency_calls = np.random.rand(n_emergency_calls, 2) * 100
hospitals = np.random.rand(n_hospitals, 2) * 100


n_ambulance_stations = 7 
ambulance_stations,labels = find_optimal_locations(n_ambulance_stations, emergency_calls)

# Combine all nodes into a single array for pairwise distance computation
all_nodes = np.concatenate((emergency_calls, hospitals, ambulance_stations))
labels = ["E"] * n_emergency_calls + ["H"] * n_hospitals + ["A"] * n_ambulance_stations
label_positions = {f"{labels[i]}{i}": pos for i, pos in enumerate(all_nodes)}


G = nx.Graph()


for i, label in enumerate(labels):
    G.add_node(f"{label}{i}", pos=all_nodes[i], node_type=label)

# Create random edges based on proximity
for i, point_i in enumerate(all_nodes):
    for j, point_j in enumerate(all_nodes[i+1:], start=i+1):  # Avoid self-loops and duplicate edges
        if np.random.rand() < connection_probability:
            distance = np.linalg.norm(point_i - point_j)
            if distance <= max_connection_distance:
                G.add_edge(f"{labels[i]}{i}", f"{labels[j]}{j}", weight=distance)

# Connect all disconnected components
connect_components(G)

content = f"{G.number_of_nodes()}\n"


for node in G.nodes(data=True):
    node_type = node[0][0]  # First character of node ID represents the type
    node_id = node[0][1:]   # The rest of the node ID
    pos = node[1]['pos']
    content += f"{node_type} {node_id} {pos[0]} {pos[1]}\n"

# Write edge information: Node1, Node2, Weight
for edge in G.edges(data=True):
    node1, node2, weight = edge
    content += f"{node1} {node2} {weight['weight']:.2f}\n"

# Display the content to be written to the file
print(content)
with open('graph_structure.txt', 'w') as f:
    f.write(content)

# Visualization
plt.figure(figsize=(12, 12))
pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['node_type'] == 'E'], node_color='blue', node_size=50, label='Emergency Calls')
nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['node_type'] == 'H'], node_color='green', node_size=100, label='Hospitals')
nx.draw_networkx_nodes(G, pos, nodelist=[n for n in G.nodes if G.nodes[n]['node_type'] == 'A'], node_color='red', node_size=100, label='Ambulance Stations')
nx.draw_networkx_edges(G, pos, width=1, alpha=0.5)
nx.draw_networkx_labels(G, pos, font_size=8, verticalalignment='bottom')

# Create legend
plt.legend(handles=[
    mpatches.Patch(color='blue', label='Emergency Calls'),
    mpatches.Patch(color='green', label='Hospitals'),
    mpatches.Patch(color='red', label='Ambulance Stations')
])

plt.title('City Map-like Graph Structure')
plt.grid(True)
plt.axis('equal') 
plt.show()

