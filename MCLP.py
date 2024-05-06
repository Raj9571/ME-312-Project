import pulp
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)  # For reproducibility
n_demand_points = 200  # Number of demand points
n_potential_locations = 20  # Number of potential ambulance station locations
service_radius = 3  # Service radius for each ambulance station
max_stations = 10  # Maximum number of ambulance stations to establish

demand_points = np.random.rand(n_demand_points, 2) * 10
potential_locations = np.random.rand(n_potential_locations, 2) * 10

# Calculate distances between demand points and potential locations
distances = np.linalg.norm(demand_points[:, None, :] - potential_locations[None, :, :], axis=2)

# Binary indicator whether a demand point is within service radius of a potential location
coverage = (distances <= service_radius).astype(int)
model = pulp.LpProblem("Maximal_Covering_Location_Problem", pulp.LpMaximize)
x = pulp.LpVariable.dicts("x", range(n_potential_locations), cat='Binary')
y = pulp.LpVariable.dicts("y", range(n_demand_points), cat='Binary')

model += pulp.lpSum(y[i] for i in range(n_demand_points))
for i in range(n_demand_points):
    model += y[i] <= pulp.lpSum(x[j] * coverage[i, j] for j in range(n_potential_locations)), f"Coverage_{i}"
model += pulp.lpSum(x[j] for j in range(n_potential_locations)) <= max_stations, "Max_Stations"


model.solve()

# Determine covered demand points
covered_demand_points = [i for i in range(n_demand_points) if y[i].value() == 1]
selected_locations = [j for j in range(n_potential_locations) if x[j].value() == 1]
plt.figure(figsize=(12, 10))

# Plot all demand points
plt.scatter(demand_points[:, 0], demand_points[:, 1], c='lightblue', label='Demand Points')

# Highlight covered demand points
if covered_demand_points:
    plt.scatter(demand_points[covered_demand_points, 0], demand_points[covered_demand_points, 1], c='blue', label='Covered Demand Points')

# Plot potential locations for ambulance stations
plt.scatter(potential_locations[:, 0], potential_locations[:, 1], marker='s', s=100, c='orange', label='Potential Stations')

# Highlight selected locations for ambulance stations
if selected_locations:
    plt.scatter(potential_locations[selected_locations, 0], potential_locations[selected_locations, 1], marker='P', s=200, c='red', label='Selected Stations')

plt.title('Ambulance Station Placement Optimization')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()
plt.grid(True)
plt.show()

