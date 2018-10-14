# Class that implements an inverted index structure
import xml.etree.ElementTree as ET
from Preprocessor import *

class InvertedIndex(object):
    '''Class that implements the positional inverted index'''

    ppr = Preprocessor()

    def __init__(self):
        '''Constructor of Class InvertedIndex. Initializes inverted index dictionary structure.'''
        self.invertedIndexDictionary = {}
        self.parseXMLFile('data/collections/mini.xml')

    def initializeTerm(self, term):
        '''Method that initializes the dictionary structure for the documents in which the term is located'''
        self.invertedIndexDictionary[term] = {}

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
            #elif docID not in self.invertedIndexDictionary[term]:
            #self.initializeDoc(term, docID)

    def parseXMLFile(self, pathToFile):
        '''Doc of func'''
        tree = ET.parse(pathToFile)
        root = tree.getroot()
        # Text = []
        for child in root:
            for node in child:
                node_tag = node.tag
                if node_tag == 'DOCNO':
                    docID = node.text
                if node_tag == 'TEXT':
                    for s in self.ppr.tokenize(node.text):
                        lowerCase = self.ppr.toLowerCase(s)
                        if (len(lowerCase) > 1): #and (self.ppr.isNotAStopword(lowerCase)):
                            self.insertTermOccurrence(lowerCase, int(docID), 4) # Put correct position through string index
                            # self.insertTermOccurrence(self.ppr.stemWordPorter(lowerCase), int(docID), 4) # Put correct position through string index




        print('lems {}'.format(len(self.invertedIndexDictionary)))
        for term in self.invertedIndexDictionary:
            counter = 0
            for doc in self.invertedIndexDictionary[term]:
                for pos in self.invertedIndexDictionary[term][doc]:
                    counter += 1
            print('Term is =  {}, Number of occurrences: {}'.format(term, counter))
                #print(self.invertedIndexDictionary[term][doc])












#pathToFile = 'data/collections/sample.xml'




#def parseXMLFile(pathToFile):
#    with open(pathToFile) as currentFile:
#        for line in currentFile:
#            if "<DOCNO>" in line:
#                print("id")

#def parseXML(pathToFile):
#    xmlTree = ET.parse(pathToFile)
#    print(xmlTree.getroot())


#parseXMLFile(pathToFile)
#parseXML(pathToFile)
