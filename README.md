# ME-312-Project
<h2>These are all the files used in the Design and Implementation of an Ambulance Dispatch System.</h2>

1. MCLP.py and optimal_location.py are used to find optimal location of Ambulance Station using MCLP algorithm and K Means Clustering
   respectively.
2. city.py generates a arbitrary city consisting of potential Emergency call locations and Hospitals and it ensures that the graph generated is connected and city like. It uses optimal location.py to output a txt file 'graph_structure.txt' that have Graph data of all potential emergencies, hospital and ambulance station (found using K means).
3. create_graph.py is used in other code files to generate a graph structure using a txt file. Text file should have first line as no. of nodes (n), next n lines should have node location and remaining lines are weights of edges between nodes.
4. animation.py is used to show animation of two ambulances moving simultaneoulsy to two emergency calls and delivering them to nearest hospitals and then again moving to next emergency calls.
5. clusters.png is image of clusters and their centroids found using optimal_location.py
6. create_graph_2.py used to take 



