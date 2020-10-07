class Graph:
    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}
    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()
    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("vertecies do not exist")
    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]
    def dft_recursive(self, starting_vertex, visited=None, path=None, results=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        This should be done using recursion.
        """
        if visited is None and path is None and results is None:
            visited = set()
            path = [starting_vertex]
            results = list()
        if len(path) >= 2:
            results.append(path)
        if path[-1] not in visited:
            visited.add(path[-1])
            for bro in self.get_neighbors(path[-1]):
                new_path = list(path) + [bro]
                results.append(new_path)
                self.dft_recursive(bro, visited, new_path, results)
        return results
def earliest_ancestor(ancestors, starting_node):
    # initializing a graph
    liniage = Graph()
    # adding the edges
    for i in ancestors:
        if i[0] not in liniage.vertices:
            liniage.add_vertex(i[0])
        if i[1] not in liniage.vertices:
            liniage.add_vertex(i[1])
        liniage.add_edge(i[1], i[0])
    # lists of paths with length greater than 1
    output = liniage.dft_recursive(starting_node)
    # length of longest list/path
    max_len_paths = max([len(p) for p in output]) if len(output) > 0 else 0
    # container for possible results
    possible_results = list()
    # loop through each path in output to eliminate those that have length that is less than the max length
    for p in output:
        if len(p) == max_len_paths:
            possible_results.append(p)
    # if length of possible results is 1, then we return the last element of that list
    if len(possible_results) == 1:
        return possible_results[0][-1]
    # else, if there's 2 or more, we compare the last elements of these arrays to check the lowest ancestor
    elif len(possible_results) > 1:
        current_ancestor = possible_results[0][-1]
        for p in possible_results:
            if p[-1] < current_ancestor:
                current_ancestor = p[-1]
        return current_ancestor
    return -1
test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
                  (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
