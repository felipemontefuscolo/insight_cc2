import json      # for reading json data
import bisect    # for the sorted list
from collections import defaultdict
from pprint import pprint

tweets = ['']
with open('../tweet_output/ft1.txt') as txt:
    tweets = txt.read().splitlines()

# Function to remove an element from a sorted list
def removeL(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect.bisect_left(a, x)
    if i != len(a) and a[i] == x:
        del a[i]
    #raise ValueError

# This class implementation was inspired by http://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self, connections):
        self._graph = defaultdict(list)
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """ Add connection between node1 and node2 """

        bisect.insort(self._graph[node1], node2)
        bisect.insort(self._graph[node2], node1)

    def removeEdge(self, node1, node2):
        removeL(self._graph[node1], node2)
        removeL(self._graph[node2], node1)
        #if node2 in self._graph[node1]: self._graph[node1].remove(node2)
        #if node1 in self._graph[node2]: self._graph[node2].remove(node1)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        #return '{}({})'.format('merda', 'merda')
        #return 'merda'

    def p(self):
        pprint(dict(self._graph))

connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),('C', 'D'), ('E', 'F'), ('F', 'C')]
g = Graph(connections)
g.p()
















