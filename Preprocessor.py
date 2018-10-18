# Class implementing the preprocessing toolkit
import re # Python regular expressions
# from stemming.porter2 import stem # Porter stemmer function
# from nltk.stem.snowball import SnowballStemmerpo
from nltk.stem import PorterStemmer

class Preprocessor(object):
    '''Class of type object that provides a basic toolkit for text preprocessing'''
    # snws = SnowballStemmer("english") # Initialize snowball stemmer - for all instances?
    stopwords = set() # Set with stopwords - O(1) search
    porter = PorterStemmer()

    def __init__(self):
        '''Constructor of Class Preprocessor'''
        self.loadStopwords()

    def tokenize(self, string):
        '''Splits argument 'string' and returns a list of the tokens. The regular expression used
        is (?!\'\b)\W+ which splits the string in every non alphanumeric character (\W+) except the
        case in which a hypostrophe is within a word (?!\'\b) e.g. don't, isn't, I'm, etc. These
        kinds of words should not be split. '''
        return re.split(r'(?!\'|\&|\-\b)\W+', string) # r stands for raw expression - test different approaches!!!

    def stemWordPorter(self, word):
        '''Stems the given word using the Porter Stemmer library'''
        return self.porter.stem(word)

    def stemWordSnowball(self, word):
        '''Stems the given word using the Porter Stemmer library'''
        return self.snws.stem(word)

    def toLowerCase(self, string):
        '''Method that receives a word and returns it with all letters in lower case'''
        return string.lower()

    def isNotAStopword(self, word):
        '''Returns true if the given word is not a stopword, otherwise false'''
        if word in self.stopwords:
            return False
        return True

    def loadStopwords(self):
        '''Method that loads all stopword terms from file and saves them to a set structure'''
        with open('data/stopwords.txt') as stopWordFile:
            self.stopwords = set(stopWordFile.read().splitlines())
