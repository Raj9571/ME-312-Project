import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx
from create_graph import recreate_graph_from_file

def load_graph(file_path):
    return recreate_graph_from_file(file_path)

def read_hospital_assignments(assignment_file_path):
    assignments = {}
    with open(assignment_file_path, 'r') as f:
        next(f)  # Skip the header line
        for line in f:
            emergency, hospital = line.strip().split(' assigned to ')
            assignments[emergency] = hospital
    return assignments

def get_node_color(node):
    if node.startswith('H'):
        return "green"
    elif node.startswith('A'):
        return "red"
    elif node.startswith('E'):
        return "blue"
    return "gray"

file_path = 'graph_structure.txt'
G = load_graph(file_path)
pos = nx.get_node_attributes(G, 'pos')

assignment_file_path = 'hospital_assignments.txt'
assignments = read_hospital_assignments(assignment_file_path)

# Assuming two ambulances for demonstration, splitting assignments between them
ambulance_assignments = {
    'Ambulance1': dict(list(assignments.items())[:len(assignments)//2]),
    'Ambulance2': dict(list(assignments.items())[len(assignments)//2:])
}

# Preparing the figure
fig, ax = plt.subplots(figsize=(10, 10))
nx.draw_networkx(G, pos, ax=ax,node_size=100, node_color=[get_node_color(n) for n in G.nodes()], font_size=8, with_labels=True)
plt.axis('off')

# Initialize markers for each ambulance
ambulance_markers = {ambulance: ax.plot([], [], 'o', markersize=15)[0] for ambulance in ambulance_assignments}
# Initialize status text for each ambulance at the top of the figure
ambulance_status_texts = {ambulance: ax.text(0.5, 1.0 - i*0.05, '', transform=ax.transAxes, ha='center') for i, ambulance in enumerate(ambulance_assignments)}

# Function to generate paths and statuses for each ambulance
def generate_ambulance_info(assignments, G):
    ambulance_info = {}
    for ambulance, tasks in assignments.items():
        info = {'path': [], 'statuses': []}
        current_location = 'A210'  # Starting point for all ambulances
        for emergency, hospital in tasks.items():
            # Get paths
            path_to_emergency = nx.shortest_path(G, source=current_location, target=emergency)
            path_to_hospital = nx.shortest_path(G, source=emergency, target=hospital)[1:] # Skip the first to avoid duplicate
            info['path'].extend(path_to_emergency + path_to_hospital)
            # Generate status messages
            for node in path_to_emergency:
                info['statuses'].append(f"heading to emergency at {emergency}")
            for node in path_to_hospital:
                info['statuses'].append(f"heading to hospital {hospital}")
            current_location = hospital
        ambulance_info[ambulance] = info
    return ambulance_info

ambulance_info = generate_ambulance_info(ambulance_assignments, G)

# Animation update function
status_title = ax.text(0.5, 1.0, '', transform=ax.transAxes, ha='center', va='top')

# Update function
def update(frame):
    title_texts = []  # List to hold current status messages
    for ambulance, info in ambulance_info.items():
        if frame < len(info['path']):
            current_node = info['path'][frame]
            x, y = pos[current_node]
            ambulance_markers[ambulance].set_data(x, y)  # Update ambulance position
            title_texts.append(f"{ambulance} {info['statuses'][frame]}")  # Append status message
    # Join all title texts and set it to the status title text object
    status_title.set_text('\n'.join(title_texts))
    # We return all the markers and the single status title text object
    return list(ambulance_markers.values()) + [status_title]

# Determine the number of frames for the animation based on the longest ambulance path
num_frames = max(len(info['path']) for info in ambulance_info.values())

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=num_frames, interval=500, blit=True)


plt.show()
