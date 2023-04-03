import json

class Node:
    def __init__(self, id, q1, q2):
        self.id = id
        self.q1 = q1
        self.q2 = q2
    def print_node_info(self):
        print("(" + str(self.q1) + ", " + str(self.q2) + ")")
        print("Id: ", self.id)

class Link:
    def __init__(self, id, source, target):
        self.id = id
        self.source = source
        self.target = target

class Graph:
    graph_id = 0
    def __init__(self, nodes, links):
        Graph.graph_id += 1
        self.id = Graph.graph_id
        self.nodes = nodes
        self.links = links
    @classmethod
    def load(cls, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        nodes = []
        links = []
        for node_json in data["nodes"]:
            node = Node(node_json['id'], node_json['q1'], node_json['q2'])
            nodes.append(node)
        for link_json in data["links"]:
            link = Link(link_json['id'], link_json['source'], link_json['target'])
            links.append(link)
        return Graph(nodes, links)
    def node_index(self, id):
        for i, node_element in enumerate(self.nodes):
            if id == node_element.id:
                return i
    def adjacency_matrix(self):
        n = self.nodes.__len__()
        adj_matrix = [[0 for i in range(n)] for j in range(n)]
        for k, link in enumerate(self.links):
            i = self.node_index(link.source)
            j = self.node_index(link.target)
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
        return adj_matrix
    def vetrex_degrees(self):
        vertex_degrees = 0
        adj_matrix = self.adjacency_matrix
        for i in range(len(adj_matrix)):
            ith_vertex_degree = 0
            for j in range(len(adj_matrix)):
                if adj_matrix[i][j] == 1 or adj_matrix[j][i] == 1:
                    c += 1
            vertex_degrees.append(ith_vertex_degree)
        return vertex_degrees
    # + show isolates
    def count_isolates(self):
        isolates_indices = []
        adj_matrix = self.adjacency_matrix
        for i, node in enumerate(self.nodes):
            count_ones = adj_matrix[i].count(1)
            if count_ones == 0:
                isolates_indices.append(i)
        return isolates_indices.count(0) 
    def vertex_count(self):
        return len(self.nodes)
    def edge_count(self):
        return len(self.links)
    def adjacency_list(self):
        n = self.nodes.__len__()
        neighbours = [[] for i in range(n)]
        for k, link in enumerate(self.links):
            i = G.node_index(link.source)
            j = G.node_index(link.target)
            neighbours[i].append(link.target)
            neighbours[j].append(link.source)
        return neighbours
