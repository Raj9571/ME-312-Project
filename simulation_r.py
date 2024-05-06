import heapq
import networkx as nx
import math
from create_graph import recreate_graph_from_file

class AmbulanceDispatch:
    def __init__(self, graph, ambulance_data):
        self.graph = graph
        self.available_ambulances = ambulance_data
        self.unavailable_ambulances = {}
        self.priority_queue = []
        self.current_time = 0  # Track the current time for dispatches
        self.was_queue_processed = False  # Track whether the queue was processed
        self.hospital_to_station = read_ambulance_station_assignments('hospital_to_station_mapping.txt')
    def simulate_one_step(self):
        # Process all calls that are scheduled for the current time
        self.process_calls_and_queue()
        # Update the status of ambulances
        self.update_available_ambulances()
        # Try to dispatch any remaining queued requests
        self.process_queued_requests()
        # Increment simulation time
        self.current_time += 1

    def find_nearby_ambulances(self, patient_node, radius=float('inf')):
        nearby_ambulances = {}
        min_distance = float('inf')
        nearest_ambulance_id = None

        for ambulance_id, ambulance_node in self.available_ambulances.items():
            try:
                path_length = nx.dijkstra_path_length(self.graph, source=ambulance_node, target=patient_node, weight='weight')  # Assuming weights represent distance/time
                if path_length <= radius:
                    nearby_ambulances[ambulance_id] = (ambulance_node, path_length)
                if path_length < min_distance:
                    min_distance = path_length
                    nearest_ambulance_id = ambulance_id
            except nx.NetworkXNoPath:
                print(f"No path from ambulance {ambulance_id} at node {ambulance_node} to patient at node {patient_node}")

        if not nearby_ambulances and nearest_ambulance_id:
            nearest_ambulance_node, nearest_distance = self.available_ambulances[nearest_ambulance_id], min_distance
            nearby_ambulances[nearest_ambulance_id] = (nearest_ambulance_node, nearest_distance)

        return nearby_ambulances


    def dispatch_ambulance(self, patient_node, hospital_node, patient_type):
        print(f"{self.current_time}: Attempting dispatch for patient at {patient_node}")
        self.update_available_ambulances()

        if not self.available_ambulances:
            print(f"{self.current_time}: No ambulances available, enqueued patient at {patient_node} with priority {self.determine_priority(patient_node, self.current_time)}")
            heapq.heappush(self.priority_queue, (self.determine_priority(patient_node, self.current_time), patient_node, hospital_node, patient_type, self.current_time))
            return


        nearby_ambulances = self.find_nearby_ambulances(patient_node)
        if not nearby_ambulances:
            print(f"No nearby ambulances found; adding to queue")
            heapq.heappush(self.priority_queue, (self.determine_priority(patient_node, self.current_time), patient_node, hospital_node, patient_type, self.current_time))
            return

        best_ambulance_id, best_cost = self.select_best_ambulance(nearby_ambulances, patient_node, hospital_node)
        if best_ambulance_id is None:
            print(f"Unable to find a suitable ambulance for dispatch; adding to queue")
            heapq.heappush(self.priority_queue, (self.determine_priority(patient_node, self.current_time), patient_node, hospital_node, patient_type, self.current_time))
            return
        nearest_station_data = self.hospital_to_station[hospital_node]
        return_time = nearest_station_data['travel_time']
        self.mark_ambulance_unavailable(best_ambulance_id, hospital_node, best_cost)
        print(f"Ambulance {best_ambulance_id} dispatched to {patient_node}, will be free at {self.current_time + best_cost+return_time}")

    def update_available_ambulances(self):
        newly_available = []
        for ambulance_id, info in list(self.unavailable_ambulances.items()):
            if info['availability_time'] <= self.current_time:
                newly_available.append(ambulance_id)
                station_location = info['station_location']  # Changed from 'hospital_location' to 'station_location'
                self.available_ambulances[ambulance_id] = station_location
                del self.unavailable_ambulances[ambulance_id]

        if newly_available:
            print(f"Ambulances {newly_available} now available and stationed accordingly.")

    def process_queued_requests(self):
        if not self.available_ambulances or not self.priority_queue:
            print(f"{self.current_time}: No processing required: No available ambulances or empty queue.")
            return

        print(f"{self.current_time}: Processing queue. Queue Length: {len(self.priority_queue)}")
        while self.priority_queue and self.available_ambulances:
            _, patient_node, hospital_node, patient_type, _ = heapq.heappop(self.priority_queue)
            self.dispatch_ambulance(patient_node, hospital_node, patient_type)

        print(f"{self.current_time}: Remaining queue length: {len(self.priority_queue)}")

    def determine_priority(self, patient_node, time):
        return time  # Negative time to prioritize earlier requests

    def select_best_ambulance(self, nearby_ambulances, patient_node, hospital_node):
        # Assume shortest path to patient plus path from patient to hospital determines best ambulance
        min_total_cost = float('inf')
        best_ambulance_id = None
        for ambulance_id, (ambulance_node, cost_to_patient) in nearby_ambulances.items():
            try:
                cost_to_hospital = nx.dijkstra_path_length(self.graph, source=patient_node, target=hospital_node, weight='weight')
                total_cost = cost_to_patient + cost_to_hospital
                if total_cost < min_total_cost:
                    min_total_cost = total_cost
                    best_ambulance_id = ambulance_id
            except nx.NetworkXNoPath:
                print(f"No path from patient at node {patient_node} to hospital at node {hospital_node}")

        return best_ambulance_id, min_total_cost if best_ambulance_id else None

    def mark_ambulance_unavailable(self, ambulance_id, hospital_node, best_cost):
        # After delivering a patient, the ambulance goes to the nearest station
        nearest_station_data = self.hospital_to_station[hospital_node]
        nearest_station = nearest_station_data['station']
        return_time = nearest_station_data['travel_time']
        self.unavailable_ambulances[ambulance_id] = {
            'station_location': nearest_station,
            'availability_time': self.current_time + best_cost + return_time
        }
        del self.available_ambulances[ambulance_id]

    
    
    def run_simulation(self, patient_calls):
        # Determine the maximum call time from patient_calls for an initial frame of reference.
        last_call_time = max(call[2] for call in patient_calls if call)
        
        # Initialize the current time and start processing.
        self.current_time = 0
        
        while self.current_time <= last_call_time or not self.is_all_processed():
            self.update_available_ambulances()
            self.process_calls_and_queue(patient_calls)
            self.process_queued_requests()

            # Only increment the current time if we haven't reached the last scheduled call time
            # or if there are still items in the queue after processing the last known time.
            if self.current_time <= last_call_time or not self.is_queue_empty():
                self.current_time += 1
            else:
                break  # Exit the loop if there are no more calls and the queue is empty after the last known call.

    def is_all_processed(self):
        # Check if the priority queue is empty and all future scheduled calls are handled.
        return len(self.priority_queue) == 0 and all(call[2] < self.current_time for call in patient_calls)

    def is_queue_empty(self):
        # Helper function to check if the priority queue is empty.
        return len(self.priority_queue) == 0
    
    def process_calls_and_queue(self, patient_calls):
        for call in patient_calls:
            if call[2] == self.current_time:  # Assuming the time is the third element in the tuple
                self.dispatch_ambulance(call[0], call[1], call[2])

def read_hospital_assignments(assignment_file_path):
    assignments = {}
    with open(assignment_file_path, 'r') as f:
        next(f)  # Skip the header line
        for line in f:
            emergency, hospital = line.strip().split(' assigned to ')
            assignments[emergency] = hospital
    return assignments

def read_ambulance_station_assignments(file_path):
    assignments = {}
    with open(file_path, 'r') as f:
        next(f)  # Skip the header line
        for line in f:
            hospital, data = line.strip().split(' assigned to ')
            station, travel_details = data.split(', Travel Time: ')
            travel_time, travel_path = travel_details.split(', path: ')
            assignments[hospital] = {'station': station, 'travel_time': float(travel_time), 'travel_path':travel_path}
    return assignments


if __name__ == "__main__":
    graph = recreate_graph_from_file('graph_structure.txt')
    assignment_file_path = 'hospital_assignments.txt'
    assignments = read_hospital_assignments(assignment_file_path)
    ambulance_data = {
    1: 'A210', 2: 'A211', 3: 'A212', 4: 'A213', 5: 'A214', 
    6: 'A215', 7: 'A216'
}
    dispatcher = AmbulanceDispatch(graph, ambulance_data)
    patient_calls = [
    ('E150', 1, 5), ('E153', 1, 10), ('E43', 1, 15), ('E120', 1, 20), 
    ('E140', 1, 25), ('E92', 1, 30), ('E101', 2, 35), ('E105', 2, 40), 
    ('E108', 3, 45), ('E112', 4, 50), ('E115', 5, 55), ('E119', 6, 60), 
    ('E123', 7, 65), ('E126', 8, 70), ('E129', 9, 75), ('E132', 10, 80),
    ('E135', 1, 85), ('E138', 2, 90), ('E142', 3, 95), ('E145', 4, 100)
]
    max_time = max(call[2] for call in patient_calls) + 500

    current_time = 0
# Determine the maximum time of the last call from patient calls
    last_call_time = max(call[2] for call in patient_calls)

    while current_time <= last_call_time or not dispatcher.is_queue_empty():
        dispatcher.current_time = current_time
        dispatcher.update_available_ambulances()
        
        # Process calls that match the current time
        for call in patient_calls:
            if call[2] == current_time:
                patient_node, hospital_node, _ = call
                hospital_node = assignments.get(patient_node, "Unknown")  # Get hospital node from assignments
                dispatcher.dispatch_ambulance(patient_node, hospital_node, _)

        # Process queued requests
        dispatcher.process_queued_requests()

        # Condition to break the loop: no more calls are scheduled and the queue is empty
        if current_time > last_call_time and dispatcher.is_queue_empty():
            break
        
        # Increment time
        current_time += 1