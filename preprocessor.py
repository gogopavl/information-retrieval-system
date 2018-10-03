import collections # To sort dictionary if wanted
import time # Calculate runtime
import json # To write index in a json format
import csv # To write index in a csv format
import sys # To read the arguments
import re # Regular expression handler
from nltk.tokenize import word_tokenize # Tokenizer
from nltk.stem import PorterStemmer # Porter stemmer

toc = time.time() # Start stopwatch

inputFile = 'data/bible.txt'
stopwordPath = 'stopwords.txt'

ps = PorterStemmer() # PorterStemmer toolkit
stopwords =[] # List of stopwords
termList = {} # This is my inverted index - Should implement it with a file! Must NOT cache list?

totalWordCounter = 0 # Total number of words read - used for Heap's law
uniqueTermCounter = 0 # Total number of unique terms - used for Heap's law

def main():
    global totalWordCounter

    ImportStopwordList(stopwordPath)
    totalWordsVsUniqueWordsFile = open("out/words_vs_unique.csv", "w") # File to write total number of words vs unique words

    with open(inputFile) as currentFile:
        for counter, line in enumerate(currentFile):
            for term in word_tokenize(line):
                termFormatted = StringFormatting(term); # Format word
                termStemmed = ps.stem(termFormatted) # Stem word
                # f.write(ps.stem(termStemmed)+'\n')
                if len(termStemmed) > 0: # Length > 0 so that I can eliminate empty strings
                    totalWordCounter += 1
                    if isNotAStopword(termStemmed):
                        AddToTermList(termStemmed) # Add term to dictionary
                    totalWordsVsUniqueWordsFile.write("%s,%s\n"%(totalWordCounter,uniqueTermCounter))

        ExportToCSV(termList)
        ExportToJSON(termList)
        totalWordsVsUniqueWordsFile.close()
        # f.close()

# Function that imports the stopwords list
def ImportStopwordList(pathToFile):
    with open(pathToFile) as stopWordFile:
        stopwords = stopWordFile.read().splitlines()

# Just removes spaces
def Tokenizer(line):
    tokenizedWordList = word_tokenize(line)
    # Must correct the 1:12 case...

# Function that formats a string - lower case, removes special characters
def StringFormatting(string):
    stringLowerCase = string.lower()
    stringFormatted = re.sub('[^A-Za-z0-9]+', '', stringLowerCase) # If char is not alphanumeric eliminate
    return stringFormatted

# Function that checks whether the word is a stopword
def isNotAStopword(string):
    if string not in stopwords:
        return True

# Check whether a term is  within a my term dictionary or not
def AddToTermList(key):
    global uniqueTermCounter
    if key in termList:
        termList[key] = termList[key]+1
    else:
        termList[key] = 1
        uniqueTermCounter += 1

# Writes index/terms and freqs to a file in CSV format
def ExportToCSV(dictionary):
    with open('out/output.csv', 'w') as output:
        for key in dictionary.keys():
            output.write("%s,%s\n"%(key,dictionary[key]))

# Writes index/terms and freqs to a file in Json format
def ExportToJSON(dictionary):
    orderedDictionary = collections.OrderedDict(sorted(termList.items()))
    jsonStruct = json.dumps(orderedDictionary)
    jsonFile = open("out/output.json","w")
    jsonFile.write(jsonStruct)
    jsonFile.close()

# Invoke main
main()
tic = time.time()
print("Total runtime = {}".format(tic-toc))
