from collections import defaultdict


class Graph(object):

    def __init__(self, connection, directed=False):
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connection(connection)

    def add_connection(self, connection):
        for first_node, second_node in connection:
            self.add(first_node, second_node)

    def add(self, first_node, second_node):
        self._graph[first_node].add(second_node)
        if not self._directed:
            self._graph[second_node].add(first_node)

    def remove(self, node):
        for elem, sets in self._graph.items():
            try:
                sets.remove(node)
            except KeyError as exc:
                pass
        try:
            del self._graph[node]
            return node
        except KeyError as exc:
            raise ValueError("Word is not found")
            pass

    def find(self, node, connections=None, results=None):
        """
        We can go deep as much as needed, currently only first level nodes are recursively fetched.
        For example, test dictionary looks like:
        {"car" : ["machine", "limo"], "machine": ["car", "auto"], "limo":["car", "wheels"]}
        For the input word "car" the system will return {'wheels', 'auto', 'machine', 'limo', 'car'},
        not just {"machine","limo"}
        """
        if node is None or not isinstance(node, str):
            raise ValueError("Node is empty or invalid type")
        first_node = self._graph[node]
        if first_node:
            if connections is None:
                connections = set(first_node)
        else:
            return None
        if results is None:
            results = set()
        for connected_nodes in first_node:
            results.add(connected_nodes)
        while connections:
            similar_nodes = connections.pop()
            return self.find(similar_nodes, connections, results)
        return results

    def exist(self, node):
        if self._graph[node]:
            return True
        return False

    def is_connected(self, first_node, second_node):
        return first_node in self._graph and second_node in self._graph[first_node]

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
