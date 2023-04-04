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


def test_vertex_and_edge_counts(graph, graph_nx):
    assert graph.vertex_count() == graph_nx.number_of_nodes(
    ) and graph.edge_count() == graph_nx.number_of_edges()


def test_vertex_degrees(graph, graph_nx):
    actual_vertex_degrees = graph.vertex_degrees()
    vd_nx_dict = dict(graph_nx.degree())
    expected_vertex_degrees = list(vd_nx_dict.values())
    assert actual_vertex_degrees == expected_vertex_degrees


def test_is_connected(graph, graph_nx):
    assert nx.is_connected(graph_nx) == graph.is_connected()


def test_subgraphs(graph, graph_nx):
    actual_subgraphs = set(frozenset(node.id for node in graph.nodes)
                           for graph in graph.subgraphs())
    expected_subgraphs = set(frozenset(graph)
                             for graph in nx.connected_components(graph_nx))
    assert actual_subgraphs == expected_subgraphs

def test_subgraphs_count(graph, graph_nx):
    actual_count = graph.subgraphs_count()
    expected_count = len(set(frozenset(graph)
                             for graph in nx.connected_components(graph_nx)))
    assert actual_count == expected_count


def test_find_isolates(graph, graph_nx):
    actual_isolates = graph.find_isolates()
    expected_isolates = list(nx.isolates(graph_nx))
    assert actual_isolates == expected_isolates


def test_eigenvector_centrality(graph, graph_nx):
    actual_centrality = graph.eigenvector_centrality()
    expected_centrality = nx.eigenvector_centrality(graph_nx)
    for id, value in actual_centrality.items():
        expected_value = expected_centrality[id]
        err = abs(expected_value-value)/(expected_value+value)
        assert err < 1


# def test_betweenness_centrality(graph, graph_nx):
#     actual_centrality = graph.betweenness_centrality()
#     expected_centrality = nx.betweenness_centrality(graph_nx)
#     assert actual_centrality == expected_centrality
