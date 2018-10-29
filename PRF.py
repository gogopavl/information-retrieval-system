from collections import OrderedDict
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
