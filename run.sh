#!/usr/bin/env bash

# I'll execute my programs, with the input directory tweet_input and output the files in the directory tweet_output
echo "running first feature:"
time python ./src/tweets_cleaned.py ./tweet_input/tweets.txt ./tweet_output/ft1.txt
echo "running second feature:"
time python ./src/average_degree.py ./tweet_output/ft1.txt ./tweet_output/ft2.txt



