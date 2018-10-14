# Class that implements an index term structure

class IndexTerm(object):
    '''Class that implements a term within the InvertedIndex structure'''

    def __init__(self, term):
        '''Constructor of Class IndexTerm'''
        self.term = term
        # self.frequency =
        self.documentList = {}

    def initialize(self, key):
        self.documentList[key]=[]

    def example(self, key, documentId, position):
        self.documentList.update({key, documentList[key].append(position)})
