# Class that implements the query processor
from Preprocessor import *
from InvertedIndex import *
import numpy as np
import collections
import operator

class QueryProcessor(object):
    '''Class that implements the query processor engine'''
    ppr = Preprocessor()

    def __init__(self):
        '''Constructor of Class QueryProcessor'''
        self.ii = InvertedIndex()
        self.docIDSet = set()  #  Later use sorted(set) to print!!!
        self.booleanQueries = []
        self.tfidfQueries = []

    def complexExpressionHandler(self, query):
        '''Method used to parse and handle the logical expression'''
        expressionSets = [] # List of sets used for AND & OR  handling
        if "AND" in query:
            for simpleExpression in query.split(' AND '):
                expressionSets.append(self.simpleExpressionHandler(simpleExpression.strip()))
            return expressionSets[0].intersection(expressionSets[1])
        elif "OR" in query:
            for simpleExpression in query.split(' OR '):
                expressionSets.append(self.simpleExpressionHandler(simpleExpression.strip()))
            return expressionSets[0].union(expressionSets[1])
        elif "#" in query:
            tempList = query.split('(')
            distance = int(re.sub('[^A-Za-z0-9]+', '', tempList[0]))
            termPair = tempList[1].split(')')[0]
            return self.proximityHandler(termPair, distance)
        else:
            # expressionSets.append(self.simpleExpressionHandler(query))
            return self.simpleExpressionHandler(query)

    def simpleExpressionHandler(self, singleExpression):
        '''Method used to return proper set'''
        if 'NOT' in singleExpression:
            standaloneTerm = singleExpression.split('NOT')[1].strip()
            if '"' in standaloneTerm:
                # call "" phrase handler
                termDocumentSet = self.phraseHandler(standaloneTerm)
                # termSet = self.ii.getTermDocumentSet(self.preprocessedTerm(standaloneTerm)) # Get set of docIDs and return complementary
            else:
                termDocumentSet = self.ii.getTermDocumentSet(self.preprocessedTerm(standaloneTerm))
            return self.docIDSet - termDocumentSet # Return complementary
        elif '"' in singleExpression:
            # translate to proximity with window = 1
            return self.phraseHandler(singleExpression)
        else:
            return self.ii.getTermDocumentSet(self.preprocessedTerm(singleExpression))

    def phraseHandler(self, phraseQuery):
        '''Method that handles phrase queries'''
        termsWithoutQuotes = re.sub(r'[\"]+', '', phraseQuery)
        termsCommaSeparated = re.sub(r' ', ',', termsWithoutQuotes)
        return self.proximityHandler(termsCommaSeparated, 1)

    def proximityHandler(self, proximityQuery, distance):
        '''Method that handles proximity queries'''
        bothTerms = proximityQuery.split(',')
        term1 = bothTerms[0].strip()
        term2 = bothTerms[1].strip()

        dict1 = self.ii.getTermDocumentDictionary(self.preprocessedTerm(term1))
        dict2 = self.ii.getTermDocumentDictionary(self.preprocessedTerm(term2))

        intersection = sorted(set(dict1.keys()).intersection(set(dict2.keys())))
        matchingDocuments = []
        for document in intersection:
            currentDocumentList1 = dict1[document]
            currentDocumentList2 = dict2[document]
            i = 0
            j = 0
            thereIsNoMatch = True
            notOutOfBounds = True
            while(thereIsNoMatch and notOutOfBounds):
                if (abs((currentDocumentList1[i] - currentDocumentList2[j])) <= distance) and ((currentDocumentList1[i] - currentDocumentList2[j]) <= 0):
                    thereIsNoMatch = False
                    matchingDocuments.append(document)
                else:
                    if currentDocumentList1[i] < currentDocumentList2[j] and i < len(currentDocumentList1) - 1:
                        i += 1
                    elif currentDocumentList1[i] >= currentDocumentList2[j] and j < len(currentDocumentList2) - 1:
                        j += 1
                    else:
                        notOutOfBounds = False
        return set(matchingDocuments)

    def executeBooleanQueries(self):
        '''Method that executes boolean queries'''
        queryResults = [] # List to store query execution results - maybe use an ordered dictionary?
        for q in self.booleanQueries:
            queryResults.append(self.complexExpressionHandler(q))
        for r in queryResults:
            if isinstance(r, set):
                print('query result = {}'.format(sorted(r)))
            else:
                print('query result = ', sorted(r))
        # Instead, invoke file writer method

    def executeTFIDFQueries(self):
        '''Method that executes TFIDF queries'''
        queryResults = [] # List to store query execution results - maybe use an ordered dictionary?
        for q in self.tfidfQueries:
            queryResults.append(self.calculateTFIDF(q))


    def calculateTFIDF(self, query):
        '''Method thats calculates the TFIDF score for a given query'''
        # len(self.docIDSet)  == N - entire collection
        queryDocumentScores = {}
        for term in self.ppr.tokenize(self.ppr.toLowerCase(query)):
            termScore = 0
            if (len(term) > 0) and (self.ppr.isNotAStopword(term)):
                termDictionary = self.ii.getTermDocumentDictionary(self.ppr.stemWordPorter(term))
                for doc, positions in termDictionary.items():
                    if doc not in queryDocumentScores:
                        queryDocumentScores[doc] = (1.0 + np.log10(len(positions))) * (np.log10(len(self.docIDSet)/len(termDictionary)))
                    else:
                        queryDocumentScores[doc] += (1.0 + np.log10(len(positions))) * (np.log10(len(self.docIDSet)/len(termDictionary)))

        tfidfRanked = sorted(queryDocumentScores.items(), key=lambda (k,v): v, reverse = True)
        # tfidfRanked = sorted(queryDocumentScores.items(), key=operator.itemgetter(1))
        print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n{}'.format(query))
        print('Rank = {}\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'.format(tfidfRanked))

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
        return listOfQueries

    def preprocessedTerm(self, word):
        '''Function that preprocesses the given word - normalizes and stems'''
        return self.ppr.stemWordPorter(self.ppr.toLowerCase(word.strip()))

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
                    docID = int(termDocEntry[0].strip())
                    self.docIDSet.add(docID) # Adding docID to set - used for NOT operation
                    listOfPositions = map(int, termDocEntry[1].strip().split(','))
                    self.ii.insertMultipleTermOccurrences(term, docID, listOfPositions) # Put correct position through string index

    def exportInvertedIndexToDirectory(self, folder):
        '''Method that invokes the ii export method'''
        self.ii.exportInvertedIndexToDirectory(folder)

    def printIISize(self):
        '''Method that invokes ii printer method'''
        self.ii.printLength()
