import json      # to read json data
from collections import defaultdict # our container
import time      # to read timestamp
import re        # regex to read timestamp
from pprint import pprint  # debug purpose
import sys # to read arguments

class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self):
        self._edges = defaultdict(lambda: 0)  # (tagA, tagB) -> counter
        self._nodes = defaultdict(lambda: 0)  # tag -> counter

    def add_edge(self, edge):
        """ Add an edge (tuple) to the graph """
        edge = tuple(sorted(edge))

        self._edges[edge] += 1
        self._nodes[edge[0]] += 1
        self._nodes[edge[1]] += 1

    def remove_edge(self, edge):
        """ remove and edge (tuple) from the graph. Does not check for errors (invalid key). """
        edge = tuple(sorted(edge))

        if self._edges[edge] == 1:
            del self._edges[edge]
        else:
            self._edges[edge] -= 1

        if self._nodes[edge[0]] == 1:
            del self._nodes[edge[0]]
        else:
            self._nodes[edge[0]] -= 1

        if self._nodes[edge[1]] == 1:
            del self._nodes[edge[1]]
        else:
            self._nodes[edge[1]] -= 1

    def average_degree(self):
        if self._nodes:
            return float(2*len(self._edges)) / float(len(self._nodes))
        else:
            return 0

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._edges))

    def p(self):
        """ debug """
        pprint(dict(self._edges))
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

    if ( len(sys.argv) < 3 ):
        print("")
        print("Using default directories")
        print("")
        InputFile = '../tweet_output/ft1.txt'
        OutputFile = '../tweet_output/ft2.txt'
    else:
        InputFile = str(sys.argv[1])
        OutputFile = str(sys.argv[2])

    ft2 = open(OutputFile, 'w')

    # Initialize our graph
    g = Graph()
   
    tweets = [   ] # list of tuples (tags, timestamp) in the past 60s

    counter = 1
    # For each tweet that arrives ...
    with open(InputFile) as File:
        for tweet in File:
            # Obs: It automatically uses buffered IO and memory management so you don't have to worry about large files.
            # Please check http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python
            #print("")
            #print("counter = ", counter)
            #counter = counter + 1
          
            # End of tweets 
            if tweet.isspace():
              break

            tweet = tweet.lower()

            # extraxt timestamp
            time = getTime(tweet) 
            tags = getTags(tweet)
 
            tweets.append( (tags, time) )
 
            # Check 60s window
            while (time - tweets[0][1] > 60):
                if len(tweets[0][0]) > 1:
                    old_edges = make_edges(tweets[0][0])
                    for i,j in old_edges:
                        g.remove_edge((i,j))
                tweets.pop(0)
            
            # If there is no edge, continue 
            if len(tags) > 1:
                # Include the new edges in the graph.
                # It comes after the removal because of the cases of repeated tweets
                edges = make_edges(tags)   
                for i,j in edges:
                    g.add_edge((i,j))
                  
              
            #print("Graph tweet #", counter-1)
            #g.p()

            ft2.write("%.2f\n" % g.average_degree())

    ft2.close()
    #g.p()
    print("") 
    print("Done. Please Check the output " + OutputFile)
    print("")

    return 0

if __name__ == "__main__":
    main()


