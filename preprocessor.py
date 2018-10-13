# Class implementing the preprocessing toolkit

# Contains methods for:
# Tokenizing text
# Formatting tokens - lower case, removing chars etc.
# Stemming terms
# Checking whether a term is a stopword or not
import re # Python regular expressionss
import nltk
from stemming.porter2 import *
# from porter2stemmer import Porter2Stemmer

class Preprocessor(object):
    '''Class of type object that provides a basic toolkit for text preprocessing'''

    def __init__(self):
        '''Empty constructor of Class Preprocessor'''

    def tokenize(self, string):
        '''Splits argument 'string' and returns a list of the tokens. The regular expression used
        is (?!\'\b)\W+ which splits the string in every non alphanumeric character (\W+) except the
        case in which a hypostrophe is within a word (?!\'\b) e.g. don't, isn't, I'm, etc. These
        kinds of words should not be split. '''
        return re.split(r'(?!\'\b)\W+', string) # r stands for raw expression

    def stemWord(self, word):
        '''Stems the given word using the Porter Stemmer library'''
        return stem(word)

    def toLowerCase(self, word):
        '''Method that receives a word and returns it with all letters in lower case'''
        return word.lower()
