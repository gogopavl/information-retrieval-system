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

qp.exportInvertedIndexToDirectory('outQP/')

end = time.time()


print('Building ii runtime = {} seconds'.format(built-start))
print('Saving ii = {} seconds'.format(saved-built))
print('Loading ii = {} seconds'.format(loaded-saved))
print('Saving ii = {} seconds'.format(end-loaded))
