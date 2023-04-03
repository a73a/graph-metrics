from graph import Graph

def test_adjacency_matrix():
    graph_instance = Graph.load('challenge_graph.json')
    result = graph_instance.adjacency_matrix()
    expected_result = []
    assert result != expected_result
