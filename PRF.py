from collections import OrderedDict
from InvertedIndex import *
import collections

class PRF(object):
    """Class implementing the Pseudo Relevance Feedback module

    Fields
    ------
    ppr : Object of type Preprocessor
        The preprocessing toolkit
    """
    def __init__(self):
        """Constructor of QueryProcessor object
        """
        self.queryDictionary = OrderedDict() # Ordered dictionary to store top k query results
        self.ii = InvertedIndex() # Inverted index

    def importResultsFromFile(self, pathToFile, k):
        """Imports top k TF-IDF results from a given file

        Parameters
        ----------
        pathToFile : String type
            The index file location
        k : Integer type
            Import the "k" first results for each query result within the file
        """
        counter = 0
        wantedID = 1
        with open(pathToFile, 'r') as resultsFile:
            for line in resultsFile:
                fields = line.split()
                queryID = int(fields[0])
                if queryID == wantedID:
                    if counter == 0:
                        self.queryDictionary[queryID] = []
                    if counter < k:
                        documentID = int(fields[2])
                        tfidfScore = float(fields[4])

                        pair = (documentID, tfidfScore) # tuple
                        self.queryDictionary[queryID].append(pair)
                        counter += 1
                    else:
                        counter = 0
                        wantedID += 1

    def importDocsFromCollection(self, pathToFile, documentIDList):
        """Extracts the content of specific documents from the collection

        Parameters
        ----------
        pathToFile : String type
            The index file location#
        documentIDList : List of Integers
            The list with all the wanted document IDs
        """
        tree = ET.parse(pathToFile)
        root = tree.getroot()
        hasHeadline = False
        position = 1 # Append all documents together so they increment the same variable
        for child in root:
            for node in child:
                node_tag = node.tag
                if node_tag == 'DOCNO':
                    docID = int(node.text)
                    if docID in documentIDList:
                        if node_tag == 'HEADLINE':
                            hasHeadline = True
                            headlineText = node.text.split("/", 1)[1].strip()
                        if node_tag == 'TEXT' or node_tag == 'Text': # So that I can parse both input files
                            # position = 1
                            text = node.text
                            if hasHeadline:
                                headlineAndText = headlineText + ' ' + text
                            else:
                                headlineAndText = text
                            for word in self.ppr.tokenize(self.ppr.toLowerCase(headlineAndText)):
                                if (len(word) > 0) and (self.ppr.isNotAStopword(word)):
                                    self.ii.insertTermOccurrence(self.ppr.stemWordPorter(word), 1, position)
                                    position += 1
                    else:
                        continue
