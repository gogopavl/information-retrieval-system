import nltk
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer
import time
import json
import collections
import csv

toc = time.time()

# Check whether a term is  within a my term dictionary or not
def AddToTermList(key):
    if key in termList:
        termList[key] = termList[key]+1
    else:
        termList[key] = 1

# Function that checks whether the word is a stopword
def isNotAStopword(string):
    if string not in stopwords:
        return True

# Function that formats a string - lower case, removes special characters
def StringFormatting(string):
    stringLowerCase = string.lower()
    stringFormatted = re.sub('[^A-Za-z0-9]+', '', stringLowerCase) # If char is not alphanumeric eliminate
    return stringFormatted

# Just removes spaces
def Tokenizer(line):
    spaceRemoved = word_tokenize(line)

# Function that imports the stopwords list
def ImportStopwordList(pathToFile):
    with open(pathToFile) as stopWordFile:
        stopwords = stopWordFile.read().splitlines()

#filepath = '/data/bible.txt'
stopwordPath = 'stopwords.txt'
stopwords =[] # List of stopwords

ImportStopwordList(stopwordPath)

ps = PorterStemmer() # PorterStemmer toolkit
termList = {} # This is my inverted index - Should implement it with a file! Must NOT cache list?

f = open("output.txt", "w")

with open('data/bible.txt') as currentFile:
    for counter, line in enumerate(currentFile):
        for term in word_tokenize(line):
            termFormatted = StringFormatting(term);
            termStemmed = ps.stem(termFormatted)
            f.write(ps.stem(termStemmed)+'\n')
            if isNotAStopword(termStemmed):
                AddToTermList(termStemmed)

    f.close()

'''
    od = collections.OrderedDict(sorted(termList.items()))
    json = json.dumps(od)
    f = open("dict.json","w")
    f.write(json)
    f.close()
'''

with open('test.csv', 'w') as f:
    for key in termList.keys():
        f.write("%s,%s\n"%(key,termList[key]))

tic = time.time()

print("Total runtime = {}".format(tic-toc))
