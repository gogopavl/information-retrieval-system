# Class that implements an inverted index structure
import xml.etree.ElementTree as ET
# Parse input file

pathToFile = 'data/collections/sample.xml'

def parseXMLFile(pathToFile):
    with open(pathToFile) as currentFile:
        for line in currentFile:
            if "<DOCNO>" in line:
                print("id")

def parseXML(pathToFile):
    xmlTree = ET.parse(pathToFile)
    print(xmlTree.getroot())


parseXMLFile(pathToFile)
parseXML(pathToFile)
