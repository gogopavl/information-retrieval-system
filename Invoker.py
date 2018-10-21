# Invoker class
from InvertedIndex import *
from QueryProcessor import *
import time

ii = InvertedIndex()
# ii.buildIndexFromFile('data/trec.sample.xml')
ii.buildIndexFromFile('data/trec.5000.xml')

ii.exportInvertedIndexToDirectory('out/index.txt')

qp = QueryProcessor()
qp.importInvertedIndexFromFile('out/index.txt')

# qp.importBooleanQuery('queries/boolean.txt')
qp.importBooleanQuery('queries/queries.boolean.txt')
# qp.importTFIDFQuery('queries/tfidf.txt')
qp.importTFIDFQuery('queries/queries.ranked.txt')


qp.executeBooleanQueries()

qp.executeTFIDFQueries()

#qp.exportInvertedIndexToDirectory('outQP/')
