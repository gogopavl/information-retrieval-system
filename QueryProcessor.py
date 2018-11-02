from collections import OrderedDict
from Preprocessor import *
from InvertedIndex import *
import numpy as np
import collections
import operator

class QueryProcessor(object):
    """Class of type object implementing a query processor engine

    Fields
    ------
    ii : Object of type InvertedIndex()
        The positional inverted index data structure
    docIDSet: Set type
        Contains all document IDs
    collectionSize : Int type
        Stores the collection size
    booleanQueriesDictionary : Ordered Dictionary data structure
        Stores all boolean queries imported from file in a (key, value) pair, where: key = query ID and value = query string
    tfidfQueriesDictionary : Ordered Dictionary data structure
        Stores all tfidf ranked queries imported from file in a (key, value) pair, where: key = query ID and value = query string
    ppr : Object of type Preprocessor
        The preprocessing toolkit
    """
    ppr = Preprocessor()
    def __init__(self):
        """Constructor of QueryProcessor object
        """
        self.ii = InvertedIndex()
        self.docIDSet = set()  # Set used to calculate complementary sets ("NOT" case) and collection size (TF-IDF)
        self.collectionSize = 0 # Variable used to store the collection size for calculating the TFIDF queries
        self.booleanQueriesDictionary = OrderedDict() # Ordered dictionary used to store boolean queries - {queryID, booleanQuery}
        self.tfidfQueriesDictionary = OrderedDict() # Ordered dictionary used to store tfidf queries - {queryID, tfidfQuery}
        self.queryTopRelevantDocumentsDictionary = OrderedDict() # Ordered dictionary to store top k query results
        self.miniIndex = InvertedIndex() # Mini Inverted index used for the PRF TF-IDF score calculation
        self.termTFIDFDictionary = {} # Dictionary to store terms and their tfidf for the PRF module

    def executeBooleanQueries(self):
        """Initializes results variable and invokes necessary methods to execute each of the given boolean queries

        Notes
        -----
        Does not return results. Instead, invokes the "writeBooleanResultsToFile" method, which exports them to a file
        """
        queryResults = OrderedDict()
        for k, v in self.booleanQueriesDictionary.items():
            queryResults[k] = self.complexExpressionHandler(v)
        self.writeBooleanResultsToFile(queryResults, 'out/results.boolean.txt')

    def complexExpressionHandler(self, query):
        """Parses and handles a logical expression.
        Afterwards, passes necessary arguments to method "simpleExpressionHandler" to retrieve subsets

        Parameters
        ----------
        query : String type
            A logical expression - e.g. "simple AND NOT complex", "this OR that", "#13(lucky, number)", etc.

        Returns
        -------
        documents : Set type
            A set containing the documents fulfilling the search criteria
        """
        expressionSets = [] # List of sets used for AND & OR expressions handling
        if " AND " in query:
            for simpleExpression in query.split(' AND '):
                expressionSets.append(self.simpleExpressionHandler(simpleExpression.strip()))
            return expressionSets[0].intersection(expressionSets[1])
        elif " OR " in query:
            for simpleExpression in query.split(' OR '):
                expressionSets.append(self.simpleExpressionHandler(simpleExpression.strip()))
            return expressionSets[0].union(expressionSets[1])
        elif "#" in query:
            tempList = query.split('(')
            distance = int(re.sub('[^0-9]+', '', tempList[0])) # Extract distance
            termPair = tempList[1].split(')')[0] # Exract term pair
            return self.proximityHandler(termPair, distance, False) # Send to proximity handler and return result
        else:
            return self.simpleExpressionHandler(query)

    def simpleExpressionHandler(self, singleExpression):
        """Determines the set corresponding to a simple expression

        Parameters
        ----------
        singleExpression : String type
            A singular expression - e.g. "NOT crime", "Scotland", etc.

        Returns
        -------
        documents : Set type
            A set containing the documents matching the singular expression
        """
        if 'NOT' in singleExpression:
            standaloneTerm = singleExpression.split('NOT', 1)[1].strip()
            if '"' in standaloneTerm:
                termDocumentSet = self.phraseHandler(standaloneTerm)
            else:
                termDocumentSet = self.ii.getTermDocumentSet(self.preprocessedTerm(standaloneTerm))
            return self.docIDSet - termDocumentSet # Return complementary
        elif '"' in singleExpression:
            return self.phraseHandler(singleExpression) # Convert to proximity with distance = 1 and specify that term occurrence order matters - isPhrase = True
        else:
            return self.ii.getTermDocumentSet(self.preprocessedTerm(singleExpression))

    def phraseHandler(self, phraseQuery):
        '''Method that handles phrase queries'''
        """Handles phrase queries - converts them to proximity type queries where distance is 1 and order matters.
        More specifically, the query "term1 term2" can be equivelant to the query #1(term1, term2) if term2 occurs always after term1, not the other way around.

        Parameters
        ----------
        phraseQuery : String type
            The phrase - e.g. "A phrase"

        Returns
        -------
        documents : Set type
            Returns the result of the proximity handler method, which are the documents containing the given phrase
        """
        termsWithoutQuotes = re.sub(r'[\"]+', '', phraseQuery)
        termsCommaSeparated = re.sub(r' ', ',', termsWithoutQuotes) # Convert to proximity format
        return self.proximityHandler(termsCommaSeparated, 1, True)

    def proximityHandler(self, proximityQuery, distance, isPhrase):
        """Handles proximity queries - implements linear merge to compare the given terms' positions

        Parameters
        ----------
        proximityQuery : String type
            The proximity query - e.g. "#13(lucky, number)"
        distance : Int type
            The distance between the two given terms
        isPhrase : Boolean type
            When it is a phrase query the order in which the two terms occur matters - changes logical condition in linear merge process

        Returns
        -------
        documents : Set type
            Returns the documents that contain the given terms within the wanted distance
        """
        termPair = proximityQuery.split(',')
        term1 = termPair[0].strip() # Extract term 1
        term2 = termPair[1].strip() # Extract term 2
        dict1 = self.ii.getTermDocumentDictionary(self.preprocessedTerm(term1))
        dict2 = self.ii.getTermDocumentDictionary(self.preprocessedTerm(term2))
        intersection = sorted(set(dict1.keys()).intersection(set(dict2.keys()))) # Search only in their intersection - no point in searching the whole collection.
        matchingDocuments = [] # List to store all matching documets
        for document in intersection:
            currentDocumentList1 = dict1[document]
            currentDocumentList2 = dict2[document]
            i = 0 # Index i for linear merge implementation
            j = 0 # Index j for linear merge implementation
            thereIsNoMatch = True # Flag to break the while loop - first occurrence satisfies since boolean search only returns docIDs, not positions
            notOutOfBounds = True # Flag to break the while loop - indeces should not exceed the
            while(thereIsNoMatch and notOutOfBounds): # Linear merge comparison
                if isPhrase:
                    condition = ((currentDocumentList1[i] - currentDocumentList2[j]) <= 0) # In case it is a phrase order matters, so the second term should appear only after the first one
                else:
                    condition = True
                if (abs((currentDocumentList1[i] - currentDocumentList2[j])) <= distance) and condition:
                    thereIsNoMatch = False
                    matchingDocuments.append(document)
                else:
                    if currentDocumentList1[i] < currentDocumentList2[j] and i < len(currentDocumentList1) - 1:
                        i += 1
                    elif currentDocumentList1[i] >= currentDocumentList2[j] and j < len(currentDocumentList2) - 1:
                        j += 1
                    else:
                        notOutOfBounds = False # Only if both indeces have exceeded the structure then break
        return set(matchingDocuments)

    def executeTFIDFQueries(self):
        """Initializes results variable and invokes necessary methods to execute each of the given tfidf ranked queries

        Notes
        -----
        Does not return results. Instead, invokes the "writeTFIDFResultsToFile" method, which exports them to a file
        """
        queryResults = OrderedDict()
        for k, v in self.tfidfQueriesDictionary.items():
            queryResults[k] = self.calculateTFIDF(v)
        self.writeTFIDFResultsToFile(queryResults, 'out/results.ranked.txt')

    def calculateTFIDF(self, query):
        """Calculates the TFIDF score for a given query

        Parameters
        ----------
        query : String type
            A free text query

        Returns
        -------
        queryDocumentScores : Dictionary type
            Dictionary containing (key, value) pairs, where key = document ID and value = document score
        """
        queryDocumentScores = {}
        for term in self.ppr.tokenize(self.ppr.toLowerCase(query)):
            termScore = 0
            termStemmed = self.ppr.stemWordPorter(term)
            if (len(term) > 0) and (self.ppr.isNotAStopword(term)):
                termDictionary = self.ii.getTermDocumentDictionary(termStemmed)
                termDictionarySize = len(termDictionary)
                if (termDictionarySize == 0): # If the term does not exist in index just ignore it
                    continue
                for doc, positions in termDictionary.items():
                    if doc not in queryDocumentScores:
                        queryDocumentScores[doc] = (1.0 + np.log10(len(positions))) * (np.log10(float(self.collectionSize)/float(termDictionarySize))) # Initialize term score
                    else:
                        queryDocumentScores[doc] += (1.0 + np.log10(len(positions))) * (np.log10(float(self.collectionSize)/float(termDictionarySize))) # Add to term score

        tfidfRanked = sorted(queryDocumentScores.items(), key=lambda (k,v): v, reverse = True)
        return queryDocumentScores

    def importBooleanQuery(self, pathToFile):
        """Imports boolean queries from files to the query dictionary

        Parameters
        ----------
        pathToFile : String type
            The path to the boolean queries file
        """
        self.booleanQueriesDictionary = self.parseQueriesFile(pathToFile)

    def importTFIDFQuery(self, pathToFile):
        """Imports tfidf ranked queries from files to the query dictionary

        Parameters
        ----------
        pathToFile : String type
            The path to the tfidf queries file
        """
        self.tfidfQueriesDictionary = self.parseQueriesFile(pathToFile)

    def writeBooleanResultsToFile(self, results, pathToFile):
        """Exports boolean results to a file following a certain structure

        Parameters
        ----------
        results : Dictionary type
            The dictionary with (key, value) pairs, where key = query ID and value = corresponding results
        pathToFile : String type
            The path leading to the output file
        """
        with open(pathToFile, 'w') as output:
            for k, v in results.items():
                if len(v) == 0:
                    output.write('{:<3}{:<3}{:<8}{:<3}{:<8}{:<3}\n'.format(k,0,'null',0,'null',0))
                for counter, doc in enumerate(sorted(v)):
                    if counter == 999:
                        break
                    output.write('{:<3}{:<3}{:<8}{:<3}{:<8}{:<3}\n'.format(k,0,doc,0,1,0))

    def writeTFIDFResultsToFile(self, results, pathToFile):
        """Exports tfidf results to a file following a certain structure

        Parameters
        ----------
        results : Dictionary type
            The dictionary with (key, value) pairs, where key = query ID and value = corresponding results
        pathToFile : String type
            The path leading to the output file
        """
        path = pathToFile.rsplit('/', 1)[0]
        if not os.path.exists(path): # Check whether the directory exists or not
            os.makedirs(path)
        with open(pathToFile, 'w') as output:
            for k, v in results.items():
                if len(v) == 0:
                    output.write('{:<3}{:<3}{:<8}{:<3}{:<8}{:<3}\n'.format(k,0,'null',0,'null',0))
                for counter, entry in enumerate(sorted(v.items(), key=lambda (k,v): v, reverse = True)):
                    if counter == 999:
                        break
                    output.write('{:<3}{:<3}{:<8}{:<3}{:<8.3f}{:<3}\n'.format(k,0,entry[0],0,entry[1],0))

    def parseQueriesFile(self, pathToFile):
        """Parses a query file

        Parameters
        ----------
        pathToFile : String type
            The query file location
        """
        dictionaryOfQueries = OrderedDict() # Temp structure to keep queries
        with open(pathToFile, 'r') as queryFile:
            for queryID, line in enumerate(queryFile):
                splittedQuery = line.split(" ", 1)
                dictionaryOfQueries[int(splittedQuery[0].strip())] = splittedQuery[1].strip()
            return dictionaryOfQueries

    def preprocessedTerm(self, word):
        """Preprocesses the given word and stems using the Preprocessor module

        Parameters
        ----------
        word : String type
            A word

        Returns
        -------
        preprocessedTerm : String type
            The stripped, lowercase and stemmed version of the given word
        """
        return self.ppr.stemWordPorter(self.ppr.toLowerCase(word.strip()))

    def expandQuery(self, numberOfTopDocuments, numberOfExpandedTerms):
        self.importResultsFromFile('out/results.ranked.txt', numberOfTopDocuments) # Import first 10 ranked results for each query

        for queryID, relevantDocumentList in self.queryTopRelevantDocumentsDictionary.iteritems():
            self.importDocsFromCollection('data/trec.sample.xml', relevantDocumentList)
            tempIndex = self.miniIndex.getIndexDictionary()
            for term, documentDictionary in tempIndex.iteritems():
                termFrequency = 0
                termScore = 0
                for document, postings in documentDictionary.iteritems():
                    termFrequency += len(postings)
                termDocumentFrequeny = len(self.ii.getTermDocumentDictionary(term))
                termTFIDF = termFrequency * np.log10(float(self.collectionSize)/float(termDocumentFrequeny)) # Simple tfidf
                self.termTFIDFDictionary[term] = termTFIDF
            result = collections.OrderedDict(sorted(self.termTFIDFDictionary.items()))
            expandedTermsString = ""
            tempIndex.clear()
            for counter, (entry, value) in enumerate(sorted(result.items(), key=lambda (k,v): v, reverse = True)):
                expandedTermsString += entry + " "
                if counter == numberOfExpandedTerms-1: # top 10 expanded terms
                    break
            print('{} {} + {}\n'.format(queryID, self.tfidfQueriesDictionary[queryID], expandedTermsString.strip()))
            self.miniIndex = InvertedIndex()
            self.termTFIDFDictionary.clear()

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
                        self.queryTopRelevantDocumentsDictionary[queryID] = []
                    if counter < k:
                        documentID = int(fields[2])
                        self.queryTopRelevantDocumentsDictionary[queryID].append(documentID)
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
                                self.miniIndex.insertTermOccurrence(self.ppr.stemWordPorter(word), 1, position)
                                position += 1
                    else:
                        continue

    ############################################
    ## Communication with InvertedIndex class ##
    ############################################

    def getCollectionSize(self):
        """Returns collection size

        Returns
        -------
        collectionSize : Integer type
            The number of documents in the collection
        """
        return self.getCollectionSize

    def importInvertedIndexFromFile(self, pathToFile):
        """Imports an already built positional inverted index from a file

        Parameters
        ----------
        pathToFile : String type
            The index file location
        """
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
        self.collectionSize = len(self.docIDSet) # Updating collection size

    def exportInvertedIndexToDirectory(self, pathToFile):
        """Invokes the inverted index export method in case the current inverted index has to be stored

        Parameters
        ----------
        pathToFile : String type
            The path leading to the output file
        """
        self.ii.exportInvertedIndexToDirectory(folder)

    def printIISize(self):
        """Prints inverted index size
        """
        self.ii.printLength()
