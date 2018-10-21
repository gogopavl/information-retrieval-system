from nltk.stem import PorterStemmer # Porter Stemmer
import re # Python regular expressions

class Preprocessor(object):
    """Class of type object that provides a basic toolkit for text preprocessing

    Fields
    ------
    stopwords : Set type
        The set with all stopwords
    porter: Object of type PorterStemmer
        The porter stemmer utility
    """
    stopwords = set() # Set with stopwords - O(1) search
    porter = PorterStemmer()

    def __init__(self):
        """Constructor of Class Preprocessor
        """
        self.loadStopwords()

    def tokenize(self, string):
        """Splits parameter 'string' and returns a list of the tokens.
        The regular expression used is (?!\&\b)\W+ which splits the string in every non alphanumeric character (\W+).
        An exception to this is when a "&" is within a word (?!\&\b) e.g. AT&T, P&G, etc.
        These kinds of words should not be split.

        Parameters
        ----------
        string : String type
            A sentence to be split

        Returns
        -------
        tokens : List of strings
            A list containing all tokens
        """
        return re.split(r'(?!\&\b)\W+', string) # r stands for raw expression

    def stemWordPorter(self, word):
        """Stems the given word using the Porter Stemmer library

        Parameters
        ----------
        word : String type
            A word to be stemmed

        Returns
        -------
        stemmedWord : String type
            The stemmed version of the given word
        """
        return self.porter.stem(word)

    def stemWordSnowball(self, word):
        """Stems the given word using the Snowball Stemmer library

        Parameters
        ----------
        word : String type
            A word to be stemmed

        Returns
        -------
        stemmedWord : String type
            The stemmed version of the given word
        """
        return self.snws.stem(word)

    def toLowerCase(self, string):
        """Receives a word and returns it with all letters in lower case

        Parameters
        ----------
        word : String type
            A word to be lowercased

        Returns
        -------
        lowercaseWord : String type
            The lowercase version of the given word
        """
        return string.lower()

    def isNotAStopword(self, word):
        """Determines whether a word is a stopword

        Parameters
        ----------
        word : String type
            A word to be checked

        Returns
        -------
        isNotStopword : Boolean type
            Returns True if the given word is not a stopword, otherwise False
        """
        if word in self.stopwords:
            return False
        return True

    def loadStopwords(self):
        """Loads all stopword terms from file and saves them to a set structure
        """
        with open('data/stopwords.txt') as stopWordFile:
            self.stopwords = set(stopWordFile.read().splitlines())
