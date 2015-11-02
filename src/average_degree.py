import json      # to read json data
import bisect    # for the sorted list
from collections import defaultdict
from pprint import pprint
import time      # to read timestamp
import re        # regex



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

    def __init__(self, connections = []):
        self._graph = defaultdict(list)
        self.add_connections(connections)

    def add_connections(self, connections):
        """ Add connections (list of tuple pairs) to graph """

        for node1, node2 in connections:
            self.add(node1, node2)
   
    def add_edge(self, edge):
        """ Add an edge (tuple) to the graph """

        bisect.insort(self._graph[edge[0]], edge[1])
        bisect.insort(self._graph[edge[1]], edge[0]) 
    
    def remove_edge(self, edge):
        """ remove and edge (tuple) from the graph """

        removeL(self._graph[edge[0]], edge[1])
        removeL(self._graph[edge[1]], edge[0])
        if not self._graph[edge[0]]:
            del self._graph[edge[0]]
        if not self._graph[edge[1]]:
            del self._graph[edge[1]]
 
    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))
        #return '{}({})'.format('merda', 'merda')
        #return 'merda'

    def p(self):
        pprint(dict(self._graph))
# ---------------------------------------------------------------------------------------------

def getTags(tweet):
    return list( {tag.strip("#") for tag in tweet.split() if tag.startswith("#")} )

def getTime(tweet):
    ts = re.search("\(timestamp\: (.*)\)", tweet).group(1)
    return time.mktime(time.strptime(ts, "%a %b %d %H:%M:%S +0000 %Y"))

def make_edges(tags):
    """ return all possible edges given a list of tags """
    conn = []
    for i in range(0, len(tags)):
        for j in range(0, i):
            conn.append((tags[i],tags[j]))
    return conn

# =============================================================================================

def main():

    #connections = [('A', 'B'), ('B', 'C'), ('B', 'D'),('C', 'D'), ('E', 'F'), ('F', 'C')]
    #g = Graph(connections)
    #g.p()
    
    # Initialize our graph
    g = Graph()
    
    with open('../tweet_output/ft1.txt') as File:
        for tweet in File:
          tags = getTags(tweet)
          if len(tags) > 1:
              first_tweet = tweet
              break
    
    tweets = [ first_tweet  ] # list of tweets with two or more hashtags in the past 60s
    
    old_time = getTime(tweets[0]) # Oldest tweet time
    old_tags = getTags(tweets[0])
    old_edges = make_edges(old_tags)
   
    ft2 = open('../tweet_output/ft2.txt', 'w')
 
    counter = 1
    # For each tweet that arrives ...
    with open('../tweet_output/ft1.txt') as File:
        for tweet in File:
            # Obs: It automatically uses buffered IO and memory management so you don't have to worry about large files.
            # Please check http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python
            print("")
            print("counter = ", counter)
            counter = counter + 1
           
            if tweet == '\n':
              break

            
 
            # extraxt timestamp
            time = getTime(tweet) 
            tags = getTags(tweet)
            edges = make_edges(tags)   
  
            # If there is no edge, continue 
            if len(tags) < 2:
                continue
 
            tweets.append(tweet)

            # Check 60s window
            if time-old_time > 60:
                for i,j in old_edges:
                    g.remove_edge((i,j))
                tweets.pop(0)
                old_time = getTime(tweets[0]) 
                old_tags = getTags(tweets[0])
                old_edges = make_edges(old_tags)

            # Include the new edges in the graph
            for i,j in edges:
                g.add_edge((i,j))
        
            #print(edges)
            print("Graph:")
            g.p()

            # compute the average degree
            ave = 0
            for key, value in g._graph.iteritems():
                ave = ave + len(value)
            #ave = ave / len(g._graph)
            print(" ===============================  Average: ", ave, len(g._graph))

    ft2.close()

if __name__ == "__main__":
    main()


