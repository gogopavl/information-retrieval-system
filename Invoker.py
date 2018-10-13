from Preprocessor import *

ppr = Preprocessor()
str = ppr.tokenize("An example of a string!!! :) Hope it works properly because it's supposed to 1234:11 do so!")
print(str)
for s in str:
    print('After: {} and stemmed: {}'.format(ppr.toLowerCase(s), ppr.stemWord(s)))
