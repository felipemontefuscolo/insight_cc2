import json      # to read json data
from collections import defaultdict
import time      # to read timestamp
import re        # regex
from pprint import pprint  # debug purpose


class Graph(object):
    """ Graph data structure, undirected by default. """

    def __init__(self):
        self._graph = defaultdict(set)

    def add_edge(self, edge):
        """ Add an edge (tuple) to the graph """
        self._graph[edge[0]].add(edge[1])
        self._graph[edge[1]].add(edge[0])
    
    def remove_edge(self, edge):
        """ remove and edge (tuple) from the graph """
        if edge[0] in self._graph:
            self._graph[edge[0]].remove(edge[1])
            if not (self._graph[edge[0]]):
                del self._graph[edge[0]]
        if edge[1] in self._graph:
            self._graph[edge[1]].remove(edge[0])
            if not (self._graph[edge[1]]):
                del self._graph[edge[1]]  

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self._graph))

    def p(self):
        """ debug """
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

    ft2 = open('../tweet_output/ft2.txt', 'w')

    # Initialize our graph
    g = Graph()
   
    with open('../tweet_output/ft1.txt') as File:
        for tweet in File:
          tags = getTags(tweet)
          if len(tags) > 1:
              first_tweet = tweet
              break
    
    tweets = [   ] # list of relevant tweets (two or more hashtags) in the past 60s
   
    # For efficiency, it keeps track of the oldest tweet 
    old_time = getTime(first_tweet) 
    old_tags = getTags(first_tweet)
    old_edges = make_edges(old_tags)
     
    counter = 1
    # For each tweet that arrives ...
    with open('../tweet_output/ft1.txt') as File:
        for tweet in File:
            # Obs: It automatically uses buffered IO and memory management so you don't have to worry about large files.
            # Please check http://stackoverflow.com/questions/8009882/how-to-read-large-file-line-by-line-in-python
            #print("")
            #print("counter = ", counter)
            #counter = counter + 1
          
            # End of tweets 
            if tweet == '\n':
              break

            # extraxt timestamp
            time = getTime(tweet) 
            tags = getTags(tweet)
            edges = make_edges(tags)   
  
            # If there is no edge, continue 
            if len(tags) > 1:
 
                tweets.append(tweet)
    
                # Check 60s window
                while (time-old_time > 60):
                    
                    for i,j in old_edges:
                        g.remove_edge((i,j))
                    tweets.pop(0)
                    old_time = getTime(tweets[0]) 
                    old_tags = getTags(tweets[0])
                    old_edges = make_edges(old_tags)

                # Include the new edges in the graph.
                # It comes after the removal because of the cases of repeated tweets
                for i,j in edges:
                    g.add_edge((i,j))

            #print("Graph tweet #", counter-1)
            #g.p()

            # compute the average degree
            ave = 0
            if len(g._graph) > 0:
                for key, value in g._graph.iteritems():
                    ave = ave + len(value)
                ave = ave / float(len(g._graph))
            ft2.write("%.2f\n" % ave)

    ft2.close()

    print("") 
    print("Done. Please Check the output ../tweet_output/ft2.txt")
    print("")

if __name__ == "__main__":
    main()


