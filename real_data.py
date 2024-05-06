import requests
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) * 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) * 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371 * c  # Radius of the Earth in kilometers
    return distance

def get_road_network_data_with_hospitals(area_name):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
        [out:json];
        area["name"="{area_name}"]->.searchArea;
        (
          way["highway"="primary"](area.searchArea);
          way["highway"="secondary"](area.searchArea);
          way["highway"="tertiary"](area.searchArea);
          relation["highway"="primary"](area.searchArea);
          relation["highway"="secondary"](area.searchArea);
          relation["highway"="tertiary"](area.searchArea);
          node["amenity"="hospital"](area.searchArea);
        );
        out body;
        >;
        out skel qt;
    """

    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching road network data with hospitals:", response.status_code)
        return None

def calculate_distances(road_network_data):
    distances = {}
    intersection_counter = 0
    intersection_ids = set()

    for element in road_network_data.get("elements", []):
        if element["type"] == "node":
            node_id = element["id"]
            lat = element["lat"]
            lon = element["lon"]
            if "tags" in element and "amenity" in element["tags"] and element["tags"]["amenity"] == "hospital":
                distances[node_id] = {"lat": lat, "lon": lon, "type": "hospital", "connections": {}}
            else:
                distances[node_id] = {"lat": lat, "lon": lon, "type": "intersection", "connections": {}}
                intersection_ids.add(node_id)

    hospitals = [node_id for node_id, data in distances.items() if data["type"] == "hospital"]

    for hospital_id in hospitals:
        nearest_intersection = min(intersection_ids, key=lambda x: haversine_distance(
            distances[hospital_id]["lat"], distances[hospital_id]["lon"],
            distances[x]["lat"], distances[x]["lon"]
        ))
        distance_to_nearest_intersection = haversine_distance(
            distances[hospital_id]["lat"], distances[hospital_id]["lon"],
            distances[nearest_intersection]["lat"], distances[nearest_intersection]["lon"]
        )
        distances[hospital_id]["nearest_intersection"] = nearest_intersection
        distances[hospital_id]["distance_to_intersection"] = distance_to_nearest_intersection
        distances[nearest_intersection]["connections"][hospital_id] = distance_to_nearest_intersection

    for element in road_network_data.get("elements", []):
        if element["type"] == "way":
            way_nodes = element["nodes"]
            for i in range(len(way_nodes) - 1):
                node1_id = way_nodes[i]
                node2_id = way_nodes[i + 1]
                if node1_id in distances and node2_id in distances:
                    node1 = distances[node1_id]
                    node2 = distances[node2_id]
                    distance = haversine_distance(node1["lat"], node1["lon"], node2["lat"], node2["lon"])
                    node1["connections"][node2_id] = distance
                    node2["connections"][node1_id] = distance

    return distances, intersection_ids

def save_to_txt(distances, intersection_ids, filename):
    with open(filename, 'w') as f:
        # Write hospital positions
        f.write("# Hospital Positions\n")
        for node_id, node_data in distances.items():
            if node_data["type"] == "hospital":
                f.write(f'H{node_id} {node_data["lat"]} {node_data["lon"]}\n')

        # Write intersection positions
        f.write("\n# Intersection Positions\n")
        for node_id, node_data in distances.items():
            if node_data["type"] == "intersection":
                f.write(f'E{node_id} {node_data["lat"]} {node_data["lon"]}\n')

        # Write connections
        f.write("\n# Connections\n")
        for node_id, node_data in distances.items():
            if node_data["type"] == "intersection":
                for connected_node_id, distance in node_data["connections"].items():
                    f.write(f'E{node_id} E{connected_node_id} {distance}\n')

        # Connect hospitals to their nearest intersection nodes
        f.write("\n# Hospital Nearest Intersection Connections\n")
        for node_id, node_data in distances.items():
            if node_data["type"] == "hospital":
                nearest_intersection = node_data["nearest_intersection"]
                distance_to_intersection = node_data["distance_to_intersection"]
                f.write(f'H{node_id} E{nearest_intersection} {distance_to_intersection}\n')

# Specify the area name (e.g., "Ujjain") for which you want to retrieve data
area_name = "Ujjain"

# Retrieve road network data with hospitals for the specified area
road_network_data_with_hospitals = get_road_network_data_with_hospitals(area_name)

if road_network_data_with_hospitals:
    # Calculate distances between nodes and extract intersection node IDs
    distances, intersection_ids = calculate_distances(road_network_data_with_hospitals)

    # Save data to text file
    save_to_txt(distances, intersection_ids, 'ujjain_map_data.txt')

    print("Map data saved to 'ujjain_map_data.txt'.")
else:
    print("No road network data with hospitals available for the specified area.")