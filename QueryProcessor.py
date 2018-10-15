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

    def importInvertedIndexFromFile(self, pathToFile):
        '''Method that import an already created positional inverted index from a file'''
        with open(pathToFile, 'r') as invertedIndexFile:
            for line in invertedIndexFile:
                if(line[0]) != '\t':
                    term = line.split(':')[0] # extract term
                else:
                    termDocEntry = line.split(':')
                    docID = termDocEntry[0].strip()
                    # print('Doc id = {}'.format(docID))
                    listOfPositions = map(int, termDocEntry[1].strip().split(','))
                    # print(listOfPositions)
                    self.ii.insertMultipleTermOccurrences(term, docID, listOfPositions) # Put correct position through string index
                    # print('size is : '.format(self.ii.getIndexLength()))

    def exportInvertedIndexToDirectory(self, folder):
        self.ii.exportInvertedIndexToDirectory(folder)

    def printIISize(self):
        self.ii.printLength()
