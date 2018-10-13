from Preprocessor import *

ppr = Preprocessor()

str = ppr.tokenize()
print(str)
for s in str:
    print('{} isNotAStopword: {}'.format(s, ppr.isNotAStopword(s)))
