from InvertedIndex import *
from QueryProcessor import *
import time

start = time.time()

ii = InvertedIndex()
ii.buildIndex()

built = time.time()

ii.exportInvertedIndexToDirectory('out/')

saved = time.time()

qp = QueryProcessor()
qp.importInvertedIndexFromFile('out/index.output')

loaded = time.time()

qp.importBooleanQuery('queries/boolean.txt')
qp.importTFIDFQuery('queries/tfidf.txt')
#qp.exportInvertedIndexToDirectory('outQP/')

end = time.time()

print('Building ii = {} seconds'.format(built-start))
print('Saving ii = {} seconds'.format(saved-built))
print('Loading ii = {} seconds'.format(loaded-saved))
print('Reading qs = {} seconds'.format(end-loaded))

# qp.printIISize()
