from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import PorterStemmer


filepath = 'bible.txt'

ps = PorterStemmer()

termList = []

f = open("output.txt", "a")

with open('stopwords.txt') as stopWordFile:
    stopwords = stopWordFile.read().splitlines()

with open(filepath) as bible:
    for counter, line in enumerate(bible):
        for term in word_tokenize(line):
            termLowCase = term.lower()
            if termLowCase not in stopwords:
                termList.append(ps.stem(termLowCase))
                f.write(ps.stem(termLowCase))

'''

with open('output.txt', 'w') as f:
    for item in sortedList:
        print >> thefile, item
'''
