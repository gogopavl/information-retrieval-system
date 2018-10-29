# Invoker class
from InvertedIndex import *
from QueryProcessor import *
from PRF import *
import time

#########################################
# Create inverted index from collection #
#########################################

# ii = InvertedIndex()
# ii.buildIndexFromFile('data/trec.sample.xml')
# ii.buildIndexFromFile('data/trec.5000.xml')

# ii.exportInvertedIndexToDirectory('out/index.txt')


#########################################
# Run query processor for given queries #
#########################################

# qp = QueryProcessor()
# qp.importInvertedIndexFromFile('out/index.txt')

# qp.importBooleanQuery('queries/boolean.txt')
# qp.importBooleanQuery('queries/queries.boolean.txt')
# qp.importTFIDFQuery('queries/tfidf.txt')
# qp.importTFIDFQuery('queries/queries.ranked.txt')

# qp.executeBooleanQueries()
# qp.executeTFIDFQueries()

#qp.exportInvertedIndexToDirectory('outQP/')

#########################################
# Pseudo relevance feedback module run  #
#########################################

prf = PRF()
prf.importResultsFromFile('out/results.ranked.txt', 10)
