import networkx as nx
from create_graph import recreate_graph_from_file

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start] = 0
    previous_nodes = {}

    unvisited_nodes = set(graph.nodes())

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])

        unvisited_nodes.remove(current_node)

        for neighbor, weight in graph[current_node].items():
            new_distance = distances[current_node] + weight['weight']
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

    return distances, previous_nodes

def assign_hospitals_to_patients(graph):
    assignments = {}
    patients = [node for node in graph.nodes() if node.startswith('E')]
    hospitals = [node for node in graph.nodes() if node.startswith('H')]

    for patient_location in patients:
        distances_to_hospitals, previous_nodes = dijkstra(graph, patient_location)
        optimal_hospital = min(hospitals, key=lambda h: distances_to_hospitals[h])
        assignments[patient_location] = optimal_hospital

    return assignments

def save_assignments_to_file(assignments, file_path):
    with open(file_path, 'w') as f:
        f.write("Assignment of Hospitals to Patients:\n")
        for patient_location, assigned_hospital in assignments:
            f.write(f"{patient_location} assigned to {assigned_hospital}\n")

# Usage:
file_path = 'graph_structure.txt'
G = recreate_graph_from_file(file_path)

# Assign hospitals to patients based on shortest distance
hospital_assignments = assign_hospitals_to_patients(G)

# Store the assignments in a list
assignment_list = []
for patient_location, assigned_hospital in hospital_assignments.items():
    assignment_list.append((patient_location, assigned_hospital))

# Save assignments to a file
output_file_path = 'hospital_assignments.txt'
save_assignments_to_file(assignment_list, output_file_path)

print("Hospital assignments have been saved to", output_file_path)
print("Assignment of Hospitals to Patients:")
for patient_location, assigned_hospital in hospital_assignments.items():
    print(patient_location, "assigned to", assigned_hospital)