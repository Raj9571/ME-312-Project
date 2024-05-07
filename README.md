# ME-312-Project
<h2>These are all the files used in the Design and Implementation of an Ambulance Dispatch System.</h2>

1. MCLP.py and optimal_location.py are used to find the optimal location of the Ambulance Station using the MCLP algorithm and K Means Clustering
   respectively.
2. city.py generates an arbitrary city consisting of potential Emergency call locations and Hospitals, ensuring that the graph generated is connected and city-like. It uses optimal location.py to output a txt file 'graph_structure.txt' with graph data for all potential emergencies, hospitals, and ambulance stations (found using K means).
3. create_graph.py is used in other code files to generate a graph structure using a txt file. The text file should have the first line as no. of nodes (n), the next n lines should have node location, and the remaining lines are weights of edges between nodes.
4. animation.py is used to show an animation of two ambulances moving simultaneously to two emergency calls, delivering them to the nearest hospitals, and then moving to the next emergency calls.
5. clusters.png is the image of clusters, and their centroids found using optimal_location.py
6. create_graph_2.py uses 'ujjain_map_data.txt' as input that generates its graph structure and outputs a file 'new_Ujjain.txt' file that removes missing info nodes and changes their node numbers.
7. generate_hospital_assignments.py is used to output a txt file 'hospital_assignments.txt' with info about which patient should be assigned to which hospital using the Dijkstra algorithm.
8. real_data.py extracts roads, houses and hospital locations from Overpass API. It uses the Haversine formula to calculate the distance between nodes and outputs a txt file 'ujjain_map_data.txt' to visualize the Ujjain city graph map.
9. sim_wrp.py is a simulation file of our ambulance dispatch strategy without the returning protocol, while simulation_rp.py is with the returning protocol, and they output log files called 'results_wrp.txt' and 'results_rp.txt', respectively.
10. update_avlbl.py is the simulation file that also stores the path of an ambulance while delivering a patient to the hospital; it's not available in simulation_rp.py and sim_wrp.py. 




