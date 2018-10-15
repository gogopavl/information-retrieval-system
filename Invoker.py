from InvertedIndex import *
from QueryProcessor import *
import time

toc = time.time()
#ii = InvertedIndex()
#ii.buildIndex()
#qp = QueryProcessor()
#qp.importInvertedIndexFromFile('out/index.output')
#qp.exportInvertedIndexToDirectory()

tic = time.time()

print('Runtime = {} seconds'.format(tic-toc))
