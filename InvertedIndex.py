from collections import OrderedDict
import xml.etree.ElementTree as ET
from Preprocessor import *
import collections
import os

class InvertedIndex(object):
    '''Class that implements the positional inverted index'''
    """Class of type object implementing a query processor engine

    Fields
    ------
    invertedIndexDictionary : Object of type InvertedIndex()
        The positional inverted index data structure
    ppr : Object of type Preprocessor
        The preprocessing toolkit
    """
    ppr = Preprocessor()

    def __init__(self):
        """Constructor of Class InvertedIndex initializes inverted index dictionary structure
        """
        self.invertedIndexDictionary = {}

    def buildIndexFromFile(self, pathToFile):
        """Invokes parsing method in order to build the positional inverted index from a given collection (file)

        Parameters
        ----------
        pathToFile : String type
            The path leading to the collection file
        """
        self.parseXMLFile(pathToFile)

    def initializeTerm(self, term):
        """Initializes the dictionary structure for the documents in which the term is located

        Parameters
        ----------
        term : String type
            A given term
        """
        self.invertedIndexDictionary[term] = OrderedDict()

    def initializeDoc(self, term , docID):
        """Initializes the list of positions that the term occurs within a document

        Parameters
        ----------
        term : String type
            A given term
        docID : Int type
            A given document ID
        """
        self.invertedIndexDictionary[term][docID] = []

    def insertTermOccurrence(self, term, docID, position):
        """Inserts an occurence of a term in the inverted index

        Parameters
        ----------
        term : String type
            A given term
        docID : Int type
            A given document ID
        position : Int type
            The position in which the term appears in the given document
        """
        if term not in self.invertedIndexDictionary:
            self.initializeTerm(term)
        if docID not in self.invertedIndexDictionary[term]:
            self.initializeDoc(term, docID)
        self.invertedIndexDictionary[term][docID].append(position)

    def insertMultipleTermOccurrences(self, term, docID, listOfPositions):
        """Inserts a list of occurences of a term in the inverted index - useful for externally building the inverted index

        Parameters
        ----------
        term : String type
            A given term
        docID : Int type
            A given document ID
        listOfPositions : List type of Ints
            The list of positions in which the term appears in the given document
        """
        if term not in self.invertedIndexDictionary:
            self.initializeTerm(term)
        if docID not in self.invertedIndexDictionary[term]:
            self.initializeDoc(term, docID)
        self.invertedIndexDictionary[term][docID].extend(listOfPositions)

    def getTermDocumentSet(self, term):
        """Returns the set of document IDs for a given term

        Parameters
        ----------
        term : String type
            A given term whose document IDs need to be retrieved

        Returns
        -------
        documentSet : Set type
            A set containing the documents that contain the given term
        """
        if term not in self.invertedIndexDictionary:
            emptySet = ()
            return emptySet
        else:
            return set(self.invertedIndexDictionary[term].keys())

    def getTermDocumentDictionary(self, term):
        """Returns the dictionary of document IDs and list of positions for a given term

        Parameters
        ----------
        term : String type
            A given term whose document IDs need to be retrieved

        Returns
        -------
        termDictionary : Dictionary type
            A dictionary containing the documents that contain the given term and the list of positions for each document in which the term appears
        """
        if term not in self.invertedIndexDictionary:
            emptyDictionary = {}
            return emptyDictionary
        else:
            return self.invertedIndexDictionary[term]

    def getIndexDictionary(self):
        """Returns the inverted index dictionary

        Returns
        -------
        invertedIndex : Dictionary type
            A dictionary containing terms, docs and postings
        """
        return self.invertedIndexDictionary

    def parseXMLFile(self, pathToFile):
        """Parses the collection of documents and updates the inverted index

        Parameters
        ----------
        pathToFile : String type
            Path leading to the file with the collection
        """
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

    def exportInvertedIndexToDirectory(self, pathToFile):
        """Exports the positional inverted index to a file within a specified directory

        Parameters
        ----------
        pathToFile : String type
            Path leading to the output file
        """
        path = pathToFile.rsplit('/', 1)[0]
        if not os.path.exists(path): # Check whether the directory exists or not
            os.makedirs(path)
        # Write operations
        with open(pathToFile, 'w') as output:
            ordered = self.orderIndex(self.invertedIndexDictionary) # shouldn't be like this!!!
            for term in ordered:#self.invertedIndexDictionary:
                output.write('{}:\n'.format(term))
                termNumOfOccurr = 0
                for doc in ordered[term]:#self.invertedIndexDictionary[term]:
                    positionList = ",".join(map(str, ordered[term][doc]))#self.invertedIndexDictionary[term][doc])) # Formatting the string with the positions
                    output.write('\t{}: {}\n'.format(doc, positionList))
                output.write('\n')

    def orderIndex(self, invertedIndex):
        """Sorts the inverted index based on its keys - used when writing the index to a file in key order (alphanumeric)

        Parameters
        ----------
        invertedIndex : InvertedIndex object type
            A positional inverted index structure

        Returns
        -------
        sortedII : InvertedIndex object type
            The key sorted version of the inverted index
        """
        return collections.OrderedDict(sorted(invertedIndex.items()))

    def printLength(self):
        '''Method that prints the number of items in the index
        '''
        print('Number of terms in II: {}'.format(len(self.invertedIndexDictionary)))
