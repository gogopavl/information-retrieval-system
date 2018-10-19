from InvertedIndex import *
from QueryProcessor import *
import time

start = time.time()

# ii = InvertedIndex()
# ii.buildIndex()

built = time.time()

# ii.exportInvertedIndexToDirectory('out/')

# ii.printLength()

saved = time.time()
qp = QueryProcessor()
qp.importInvertedIndexFromFile('out/index.5000.output')

loaded = time.time()

print('Building ii = {} seconds'.format(built-start))
print('Saving ii = {} seconds'.format(saved-built))
print('Loading ii = {} seconds'.format(loaded-saved))

# qp.importBooleanQuery('queries/boolean.txt')
qp.importBooleanQuery('queries/queries.boolean.txt')
# qp.importTFIDFQuery('queries/tfidf.txt')
qp.importTFIDFQuery('queries/queries.ranked.txt')

execute = time.time()

print('BOOLEAN QUERIES\n')
qp.executeBooleanQueries()
print('\nTFIDF QUERIES\n')
qp.executeTFIDFQueries()

#qp.exportInvertedIndexToDirectory('outQP/')

end = time.time()

print('All queries executed in = {} seconds'.format(end-execute))

# qp.printIISize()
