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
    
    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        
        if visited is None:
            visited = set()
        
        v = starting_vertex
        
        if v not in visited:

            result = v
            visited.add(v)
            
            for  bro in self.get_neighbors(v):
                
                if bro is not None:
                    
                    result = self.dft_recursive(bro,visited)
                else:
                    return v
            return result


def earliest_ancestor(ancestors, starting_node):
    
    liniage = Graph()
    for i in ancestors:
            if i[0] not in liniage.vertices:
                liniage.add_vertex(i[0])
            if i[1] not in liniage.vertices:
                liniage.add_vertex(i[1])
            liniage.add_edge(i[1],i[0])
    
    output = liniage.dft_recursive(starting_node)
    if output == starting_node:
        output = -1
        
    
    return output  

test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]

print(earliest_ancestor(test_ancestors,6))