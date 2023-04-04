import json
import math
import collections


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
        self.n = len(nodes)
        self.nodes = nodes
        self.links = links
        self.adjacency_matrix = self._adjacency_matrix()
        self.adjacency_list = self._adjacency_list()
        self.adjacency_list_indexes = self._adjacency_list_indexes()
        self.links_by_node_indexes = {}
        for link in self.links:
            source_index = self.node_index(link.source)
            target_index = self.node_index(link.target)
            self.links_by_node_indexes[(source_index, target_index)] = link
            self.links_by_node_indexes[(target_index, source_index)] = link

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
            link = Link(link_json['id'],
                        link_json['source'], link_json['target'])
            links.append(link)
        return Graph(nodes, links)

    def node_index(self, id):
        for i, node_element in enumerate(self.nodes):
            if id == node_element.id:
                return i

    def _adjacency_matrix(self):
        adj_matrix = [[0 for i in range(self.n)] for j in range(self.n)]
        for k, link in enumerate(self.links):
            i = self.node_index(link.source)
            j = self.node_index(link.target)
            adj_matrix[i][j] = 1
            adj_matrix[j][i] = 1
        return adj_matrix

    def _adjacency_list(self):
        neighbours = [[] for i in range(self.n)]
        for k, link in enumerate(self.links):
            i = self.node_index(link.source)
            j = self.node_index(link.target)
            neighbours[i].append(link.target)
            neighbours[j].append(link.source)
        return neighbours

    def _adjacency_list_indexes(self):
        neighbours = [[] for i in range(self.n)]
        for k, link in enumerate(self.links):
            i = self.node_index(link.source)
            j = self.node_index(link.target)
            neighbours[i].append(j)
            neighbours[j].append(i)
        return neighbours

    def find_isolates(self):
        isolates_indices = []
        isolates = []
        for i, node in enumerate(self.nodes):
            count_ones = self.adjacency_matrix[i].count(1)
            if count_ones == 0:
                isolates.append(node)
                isolates_indices.append(i)
        return isolates
    # + show isolates

    def vertex_count(self):
        return len(self.nodes)

    def edge_count(self):
        return len(self.links)

    def vertex_degrees(self):
        vertex_degrees = []
        for i in range(len(self.adjacency_matrix)):
            ith_vertex_degree = 0
            for j in range(len(self.adjacency_matrix)):
                if self.adjacency_matrix[i][j] == 1 or self.adjacency_matrix[j][i] == 1:
                    ith_vertex_degree += 1
            vertex_degrees.append(ith_vertex_degree)
        return vertex_degrees

    def is_connected(self):
        visited = set()
        to_visit = set()
        to_visit.add(0)
        while to_visit:
            current_idx = to_visit.pop()
            visited.add(current_idx)
            for neighbour in self.adjacency_list_indexes[current_idx]:
                if neighbour not in visited:
                    to_visit.add(neighbour)
        return len(visited) == self.n

    def subgraphs(self):
        node_indexes = set(i for i in range(self.n))
        subgraphs = []

        while node_indexes:
            i = node_indexes.pop()
            to_visit = set([i])
            nodes = []
            links = []

            while to_visit:
                i = to_visit.pop()
                nodes.append(self.nodes[i])

                for j in self.adjacency_list_indexes[i]:
                    if j in node_indexes:
                        to_visit.add(j)
                        node_indexes.remove(j)
                        links.append(self.links_by_node_indexes[(i, j)])
            subgraphs.append(Graph(nodes, links))
        return subgraphs
    
    def subgraphs_count(self):
        return len(self.subgraphs())

    def eigenvector_centrality(self):
        # use power iteration method to compute largest eigenvalue
        eigenvector = [1/math.sqrt(self.n) for i in range(self.n)]

        error_margin = 1e-2
        while True:
            # compute the matrix-vector product A * x
            Ax = []
            for i in range(self.n):
                _sum = 0
                for j in range(self.n):
                    _sum += self.adjacency_matrix[i][j] * eigenvector[j]
                Ax.append(_sum)

            # compute the new eigenvector centrality vector
            norm = math.sqrt(sum(x ** 2 for x in Ax))
            new_eigenvector = [x/norm for x in Ax]
            # check for convergence
            max_error = max(
                abs(new_eigenvector[i] - eigenvector[i])
                for i in range(self.n)
            )
            if max_error < error_margin:
                break
            eigenvector = new_eigenvector

        eigenvectors_dict = {}
        for i in range(self.n):
            eigenvectors_dict[self.nodes[i].id] = eigenvector[i]
        return eigenvectors_dict
    
    # def betweenness_centrality(self):
    #     # brandes algorithm for betweenness centrality in unweighted graphs
    #     betweenness = [0 for i in range(self.n)]
    #     for s in range(self.n):
    #         print(s, "/", self.n)
    #         S = []
    #         P = [[] for i in range(self.n)]
    #         sigma = [0 for i in range(self.n)]
    #         sigma[s] = 1
    #         d = [-1 for i in range(self.n)]
    #         d[s] = 0
    #         Q = collections.deque()
    #         Q.append(s)
    #         while len(Q) > 0:
    #             # popleft here because Q is a queue
    #             v = Q.popleft()
    #             S.append(v)
    #             for w in self.adjacency_list_indexes[v]:
    #                 # w found first time?
    #                 if d[w] < 0:
    #                     Q.append(w)
    #                     d[w] = d[v] + 1
    #                 # shortest path to w via v?
    #                 if d[w] == d[v] + 1:
    #                     sigma[w] += sigma[v]
    #                     P[w].append(v)
    #         delta = [0 for i in range(self.n)]
    #         # S returnes nodes in order of non-increasing distance from s
    #         while len(S) > 0:
    #             # pop here because S is a stack
    #             w = S.pop()
    #             for v in P[w]:
    #                 delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
    #             if w != s:
    #                 betweenness[w] += delta[w]
                    
    #     betweenness_dict = {}
    #     for i in range(self.n):
    #         betweenness_dict[self.nodes[i].id] = betweenness[i]
    #     return betweenness_dict
