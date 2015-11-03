import json  # to read json data
import sys # to read arguments


def isUnicode(s):
    try:
        s.decode('ascii')
    except:
        return True
    else:
        return False

def main():

    if ( len(sys.argv) < 3 ):
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
    
    print("")
    print("Done. Please check the output " + OutputFile)
    print("")

    return 0

if __name__ == "__main__":
    main()
