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
        self.docIDSet = set()  #  Later use sorted(set) to print!!!
        self.booleanQueries = []
        self.tfidfQueries = []

    def complexExpressionHandler(self, query):
        '''Method used to parse and handle the logical expression'''
        expressionSets = [] # List of sets
        if "AND" in query:
            # print('AND Q: {}'.format(query))
            for simpleExpression in query.split('AND'):
                expressionSets.append(self.simpleExpressionHandler(simpleExpression.strip()))
            return expressionSets[0].intersection(expressionSets[1])
        elif "OR" in query:
            for simpleExpression in query.split('OR'):
                expressionSets.append(self.simpleExpressionHandler(simpleExpression.strip()))
            return expressionSets[0].union(expressionSets[1])
        elif "#" in query:
            tempList = query.split('(')
            distance = int(re.sub('[^A-Za-z0-9]+', '', tempList[0]))
            termPair = tempList[1].split(')')[0]
            self.proximityHandler(termPair, distance)
        else:
            expressionSets.append(self.simpleExpressionHandler(query))
        return expressionSets

    def simpleExpressionHandler(self, singleExpression):
        '''Method used to return proper set'''
        if 'NOT' in singleExpression:
            standaloneTerm = singleExpression.split('NOT')[1].strip()
            termSet = self.ii.getTermDocumentSet(self.preprocessedTerm(standaloneTerm)) # Get set of docIDs and return complementary
            return self.docIDSet - termSet # Return complementary
        elif '"' in singleExpression:
            # translate to proximity with window = 1
            print('" in expression: {}'.format(self.preprocessedTerm(singleExpression)))
            pass
        else:
            return self.ii.getTermDocumentSet(self.preprocessedTerm(singleExpression))

    def phraseHandler(self, phraseQuery):
        '''Method that handles phrase queries'''
        # call proximity for diff = 1
        pass

    def proximityHandler(self, proximityQuery, distance):
        '''Method that handles proximity queries'''
        bothTerms = proximityQuery.split(',')
        term1 = bothTerms[0].strip()
        term2 = bothTerms[1].strip()
        dict1 = self.ii.getTermDocumentDictionary(self.preprocessedTerm(term1))
        dict2 = self.ii.getTermDocumentDictionary(self.preprocessedTerm(term2))

        intersection = sorted(set(dict1.keys()).intersection(set(dict2.keys())))

        for document in intersection:
            # TODO implement linear merge!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

            print('///////////DOC {} D1 positions{}'.format(document, dict1[document]))
            print('///////////DOC {} D2 positions{}'.format(document, dict2[document]))

    def executeBooleanQueries(self):
        '''Method that handles queries'''
        queryResults = [] # List to store query execution results - maybe use an ordered dictionary?
        for q in self.booleanQueries:
            queryResults.append(self.complexExpressionHandler(q))
            # queryResults += self.complexExpressionHandler(q)
        # for r in queryResults:
        #    print(r)
        # Instead, invoke file writer method

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
        return self.ppr.stemWordPorter(self.ppr.toLowerCase(word))


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
