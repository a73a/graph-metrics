from graph import Graph
import networkx as nx
import json
import itertools

graph = Graph.load('challenge_graph.json')
eigenvector_centrality = graph.eigenvector_centrality()

sorted_nodes = sorted(eigenvector_centrality, key=eigenvector_centrality.get, reverse=True)

print("Rank\tNode ID\tEigenvector Centrality")
for i, node in enumerate(sorted_nodes[:10]):
    print(f"{i+1}\t{node}\t{eigenvector_centrality[node]}")
