import json  # to read json data
import sys # to read arguments
import string # to remove escape characters 
from HTMLParser import HTMLParser # replace &gt;, etc.

def isUnicode(s):
    try:
        s.decode('ascii')
    except:
        return True
    else:
        return False

def main():

    # Used to remove escape characters. Source: http://stackoverflow.com/questions/8115261/how-to-remove-all-the-escape-sequences-from-a-list-of-strings
    escapes = ''.join([chr(char) for char in range(1, 32)])
    estable = 31 * ' '
 
    parser = HTMLParser()

    if ( len(sys.argv) < 3 ):
        print("")
        print("Using default directories")
        print("")
        InputFile = '../tweet_input/tweets.txt'
        OutputFile = '../tweet_output/ft1.txt'
    else:
        InputFile = str(sys.argv[1])
        OutputFile = str(sys.argv[2])

    # Create a vector of tweets, i.e., each element is a tweet 
    tweets = []
    with open(InputFile) as txt:
        tweets = txt.read().splitlines()
    
    # Output file
    ft1 = open(OutputFile, 'w')
   
    num_invalid_tweets = 0
    num_unicodes = 0
    for tt in tweets:
        data = json.loads(tt)
        try: #ignore invalid tweets
            txt = data['text']
        except:
            num_invalid_tweets += 1
            continue
        else:
            if isUnicode(txt):
                 num_unicodes = num_unicodes+1
                 txt = txt.encode('ascii', 'ignore')
            txt = parser.unescape(txt) # replace &gt;, etc.
            txt = str(txt).translate(string.maketrans(escapes, estable)).lower()
            ft1.write(txt + " (timestamp: " + data['created_at'] + ")\n")
    
    ft1.write('\n' + str(num_unicodes) + ' tweets contained unicode.\n')
    
    ft1.close()
    
    print("")
    print("Done. Please check the output " + OutputFile)
    #print("# of invalid tweets: " + str(num_invalid_tweets))
    print("")

    return 0

if __name__ == "__main__":
    main()
