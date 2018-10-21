# TTDS Assignment

## Dependencies

The assignment was completed using Python 2.7 on Anaconda, since that's the version in the DICE machines.

Libraries and packages used (in alphabetical order):
- collections
- nltk.stem
- numpy
- operator
- os
- re
- time
- xml.etree.ElementTree

## Folder contents

- data/ : Folder containing the collection files, as well as the stopwords list file
- out/ : Folder in which the program's output is stored (positional inverted index, boolean & tfidf queries results)
- queries/ : Folder containing given query files
- Invoker.py : Python script that runs implementation
- Preprocessor.py : Class providing preprocessing toolkit
- InvertedIndex.py : Class representing the positional inverted index structure
- QueryProcessor.py : Class implementing the query processor engine

## Running the program

From a shell run the Invoker script ("python .\Invoker.py")

### Notes

The positional inverted index output file is by default stored at "out/output.index".
The path can be altered from within the "Invoker.py" script.

By default query input file names are the given ones ("queries.boolean.txt" and "queries.ranked.txt"). 
Nonetheless, these can be altered from within the "Invoker.py" script.

As asked, the positional inverted index is loaded from the file, not built.
If wanted, the commands to build the index can be un-commented out in the "Invoker.py" script.



