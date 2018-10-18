# Class that implements an inverted index structure
import xml.etree.ElementTree as ET
from Preprocessor import *
import collections
from collections import OrderedDict
import os

class InvertedIndex(object):
    '''Class that implements the positional inverted index'''

    ppr = Preprocessor()

    def __init__(self):
        '''Constructor of Class InvertedIndex. Initializes inverted index dictionary structure.'''
        self.invertedIndexDictionary = {}

    def buildIndex(self):
        '''Method that invokes functions in order to build the positional inverted index'''
        self.parseXMLFile('data/trec.sample.xml')

    def initializeTerm(self, term):
        '''Method that initializes the dictionary structure for the documents in which the term is located'''
        self.invertedIndexDictionary[term] = OrderedDict()

    def initializeDoc(self, term , docID):
        '''Method that initializes the list of positions that the term occurs within a document'''
        self.invertedIndexDictionary[term][docID] = []

    def insertTermOccurrence(self, term, docID, position):
        '''Method that inserts an occurence of a term in the inverted index'''
        if term not in self.invertedIndexDictionary:
            self.initializeTerm(term)
        if docID not in self.invertedIndexDictionary[term]:
            self.initializeDoc(term, docID)
        self.invertedIndexDictionary[term][docID].append(position)

    def insertMultipleTermOccurrences(self, term, docID, listOfPositions):
        '''Method that inserts a list of occurences of a term in the inverted index - useful for externaly building the inverted index'''
        if term not in self.invertedIndexDictionary:
            self.initializeTerm(term)
        if docID not in self.invertedIndexDictionary[term]:
            self.initializeDoc(term, docID)
        self.invertedIndexDictionary[term][docID].extend(listOfPositions)

    def getTermDocumentSet(self, term):
        '''Method that returns the set of document ids for a given term'''
        return set(self.invertedIndexDictionary[term].keys())

    def getTermDocumentDictionary(self, term):
        '''Method that returns the dictionary of document ids and positions for a given term'''
        return self.invertedIndexDictionary[term]

    def parseXMLFile(self, pathToFile):
        '''Method that parses the collection of documents and updates the inverted index'''
        tree = ET.parse(pathToFile)
        root = tree.getroot()
        hasHeadline = False
        for child in root:
            for node in child:
                node_tag = node.tag
                if node_tag == 'DOCNO':
                    docID = int(node.text)
                if node_tag == 'HEADLINE':
                    hasHeadline = True
                    headlineText = node.text.split("/", 1)[1].strip()
                if node_tag == 'TEXT' or node_tag == 'Text': # So that I can parse both input files
                    position = 1
                    text = node.text
                    if hasHeadline:
                        headlineAndText = headlineText + ' ' + text
                    else:
                        headlineAndText = text
                    for word in self.ppr.tokenize(self.ppr.toLowerCase(headlineAndText)):
                        if (len(word) > 0) and (self.ppr.isNotAStopword(word)):
                            self.insertTermOccurrence(self.ppr.stemWordPorter(word), docID, position)
                            position += 1

    def exportInvertedIndexToDirectory(self, folder):
        '''Method that exports the positional inverted index to a file within a specified directory'''
        if not os.path.exists(folder): # Check whether the directory exists or not
            os.makedirs(folder)
        filename = 'index.output'
        if folder == 'outQP/':
            filename = 'qp.out'
        # Write operations
        with open(folder + filename, 'w') as output:
            ordered = self.orderIndex(self.invertedIndexDictionary) # shouldn't be like this!!!
            for term in ordered:#self.invertedIndexDictionary:
                output.write('{}:\n'.format(term))
                termNumOfOccurr = 0
                for doc in ordered[term]:#self.invertedIndexDictionary[term]:
                    positionList = ",".join(map(str, ordered[term][doc]))#self.invertedIndexDictionary[term][doc])) # Formatting the string with the positions
                    output.write('\t{}: {}\n'.format(doc, positionList))
                output.write('\n')

    def orderIndex(self, invertedIndex):
        '''Method that orders the inverted index based on its keys'''
        return collections.OrderedDict(sorted(invertedIndex.items()))

    def printLength(self):
        '''Method that return the number of items in the index'''
        print('my length is: {}'.format(len(self.invertedIndexDictionary)))
