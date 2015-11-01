import json  # to read json data

def isUnicode(s):
    try:
        s.decode('ascii')
    except:
        return True
    else:
        return False

# Create a vector of tweets, i.e., each element is a tweet 
tweets = []
with open('../tweet_input/tweets.txt') as txt:
    tweets = txt.read().splitlines()

# Output file
ft1 = open('../tweet_output/ft1.txt', 'w')

num_unicodes = 0
for tt in tweets:
    data = json.loads(tt)
    txt = data['text']
    if isUnicode(txt):
        num_unicodes = num_unicodes+1
        txt = txt.encode('ascii', 'ignore')
    ft1.write(txt + " (timestamp: " + data['created_at'] + ")\n")

ft1.write('\n' + str(num_unicodes) + ' tweets contained unicode.\n')

ft1.close()
