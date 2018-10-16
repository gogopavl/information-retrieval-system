# Class that implements the query processor

# Should support
# 1 Boolean search
# 2 Phrase search
# 3 Proximity search
# 4 Ranked results with TFIDF model
from Preprocessor import *
from InvertedIndex import *
import collections

class QueryProcessor(object):
    '''Class that implements the query processor engine'''
    ppr = Preprocessor()

    def __init__(self):
        '''Constructor of Class QueryProcessor'''
        self.ii = InvertedIndex()
        self.booleanQueries = []
        self.tfidfQueries = []

    def importBooleanQuery(self, pathToFile):
        '''Method to save the queries in the structure'''
        self.booleanQueries = self.parseQueriesFile(pathToFile)

    def importTFIDFQuery(self, pathToFile):
        '''Method to save the queries in the structure'''
        self.tfidfQueries = self.parseQueriesFile(pathToFile)

    def parseQueriesFile(self, pathToFile):
        '''Method to read the a query file'''
        listOfQueries = []
        with open(pathToFile, 'r') as queryFile:
            for line in queryFile:
                listOfQueries.append(line.split(" ", 1)[1].strip())
        print(listOfQueries)
        return listOfQueries

    ################################################################################################################
    ## COMM WITH INVERTED INDEX
    ################################################################################################################
    def importInvertedIndexFromFile(self, pathToFile):
        '''Method that import an already created positional inverted index from a file'''
        with open(pathToFile, 'r') as invertedIndexFile:
            for line in invertedIndexFile:
                if(line[0]) != '\t':
                    term = line.split(':')[0] # extract term
                else:
                    termDocEntry = line.split(':')
                    docID = termDocEntry[0].strip()
                    listOfPositions = map(int, termDocEntry[1].strip().split(','))
                    self.ii.insertMultipleTermOccurrences(term, docID, listOfPositions) # Put correct position through string index

    def exportInvertedIndexToDirectory(self, folder):
        '''Method that invokes the ii export method'''
        self.ii.exportInvertedIndexToDirectory(folder)

    def printIISize(self):
        '''Method that invokes ii printer method'''
        self.ii.printLength()
