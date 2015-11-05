Insight Data Engineering - Coding Challenge Solution
====================================================

This solution was implemented in Python 2.7 and it uses the following libraries:

* json
* collections
* time
* re
* pprint
* sys
* string
* HTMLParser

Those libraries are very well known in Python community.

This code was tested on my Mac OS Yosemite with Python 2.7.9.

Implementation Details:
----------------------

The graph is represented by an edge list (as suggested by the challenge description), and the data structure
is composed by two dictionaries encapsulated by the class Graph, which constructor is:

    def __init__(self):
        self._edges = defaultdict(lambda: 0)  # (tagA, tagB) -> counter
        self._nodes = defaultdict(lambda: 0)  # tag -> counter

In this way, we can use the [Handshaking lemma](https://en.wikipedia.org/wiki/Degree_(graph_theory)#Handshaking_lemma) to compute the average degree:

    average degree = 2 * num edges / num nodes

where the nodes are the hashtags.

Each edge and node has a "counter" associated because it can have multiple tweets referencings the same tags.

Comments about the output:
---------------------
* Some tweets in the file `tweets.txt` does not follow the format specified in the challenge description. Those tweets are ignored.
* Some tweets can be empty after the cleaning step (e.g., those with only unicode characters). Those tweets ARE considered by the code `average_degree.py`

Testing:
-------

The code output is validated with a hand-made input and compared to expected outputs (files `ft1_test1.txt` and `ft2_test1.txt`). This is not a sophisticated unit test, but it is enough considering the project size.

In my laptop, the code (cleaning and computing the average degree together) takes about 1.194s to process the file `tweets.txt`, which contains 10k tweets.

