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
    def __init__(self, id, nodes, links):
        self.id = id
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
        return Graph(1, nodes, links)
    def node_index(self, id):
        for i, node_element in enumerate(self.nodes):
            if id == node_element.id:
                return i
    def adjacency_matrix(self):
        n = G.nodes.__len__()
        adj_matrix = [[0 for i in range(n)] for j in range(n)]
        for k, link in enumerate(self.links):
            i = G.node_index(self.links[k].source)
            j = G.node_index(self.links[k].target)
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
        return adj_matrix
    def vertex_counts(self):
        return len(self.nodes)
    def edge_counts(self):
        return len(self.links)
    