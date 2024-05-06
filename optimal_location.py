# optimal_locations.py

from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt

def find_optimal_locations(n_clusters, emergency_call_locations):
 
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    kmeans.fit(emergency_call_locations)
    # Return the centroids of the clusters
    return kmeans.cluster_centers_, kmeans.labels_

def plot_optimal_locations(emergency_call_locations, optimal_locations, labels):
    plt.scatter(emergency_call_locations[:, 0], emergency_call_locations[:, 1], c=labels, cmap='viridis', alpha=0.5, label='Emergency Calls')
    plt.scatter(optimal_locations[:, 0], optimal_locations[:, 1], c='red', marker='X', s=100, label='Optimal Ambulance Stations')
    plt.title('Optimal Ambulance Station Locations and Clusters')
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    np.random.seed(42)
    # Example usage with randomly generated emergency call locations
    n_emergency_calls = 200
    emergency_call_locations = np.random.rand(n_emergency_calls, 2) * 100
    n_ambulance_stations = 7
    optimal_locations,labels = find_optimal_locations(n_ambulance_stations, emergency_call_locations)
    print("Optimal ambulance station locations:")
    print(optimal_locations)
    plot_optimal_locations(emergency_call_locations, optimal_locations, labels)