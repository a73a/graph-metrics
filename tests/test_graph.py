from graph import Graph
import json
import pytest
import networkx as nx

@pytest.fixture
def graph():
    G = Graph.load('challenge_graph.json')
    return G

@pytest.fixture
def graph_nx():
    with open('challenge_graph.json', 'r') as f:
        data = json.load(f)
    G_nx = nx.Graph()
    for node in data['nodes']:
        G_nx.add_node(node['id'])
    for edge in data['links']:
        G_nx.add_edge(edge['source'], edge['target'])
    return G_nx
    
# 1:
def test_vertex_and_edge_counts(graph, graph_nx):
    assert graph.vertex_count() == graph_nx.number_of_nodes() and graph.edge_count() == graph_nx.number_of_edges() 
    
# 2:
def test_vertex_degrees(graph, graph_nx):
    vertex_degrees = graph.vertex_degrees()
    vd_nx_dict = dict(graph_nx.degree())
    vertex_degrees_nx = list(vd_nx_dict.values())
    assert vertex_degrees == vertex_degrees_nx
