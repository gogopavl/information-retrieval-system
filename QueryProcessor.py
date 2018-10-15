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
    # ii = InvertedIndex()

    def __init__(self):
        '''Constructor of Class QueryProcessor'''
        self.ii = InvertedIndex()

    def importInvertedIndexFromFile(self, pathToFile):
        '''Method that import an already created positional inverted index from a file'''
        with open(pathToFile, 'r') as invertedIndexFile:
            for counter, line in enumerate(invertedIndexFile):
                if(line[0]) != '\t':
                    term = line.split(':')[0] # extract term
                    print(term)
                else:
                    termDocEntry = line.split(':')
                    docID = termDocEntry[0].strip()
                    print('Doc id = {}'.format(docID))
                    listOfPositions = map(int, termDocEntry[1].strip().split(','))
                    print(listOfPositions)
                    self.ii.insertMultipleTermOccurrences(term, docID, listOfPositions) # Put correct position through string index
                if counter == 100:
                    break

    def exportInvertedIndexToDirectory(self):
        '''Method that exports the positional inverted index to a file within a specified directory'''
        if not os.path.exists('out/'): # Check whether the directory exists or not
            os.makedirs('out/')
        # Write operations
        with open('out/queryProcessor.out', 'w') as output:
            ordered = self.orderIndex(self.ii) # shouldn't be like this!!!
            for term in ordered:#self.invertedIndexDictionary:
                output.write('{}:\n'.format(term))
                termNumOfOccurr = 0
                for doc in ordered[term]:#self.invertedIndexDictionary[term]:
                    positionList = ",".join(map(str, ordered[term][doc]))#self.invertedIndexDictionary[term][doc])) # Formatting the string with the positions
                    output.write('\t{}: {}\n'.format(doc, positionList))

    def orderIndex(self, invertedIndex):
        '''Method that orders the inverted index based on its keys'''
        return collections.OrderedDict(sorted(invertedIndex.items()))
