import nltk
from nltk.tokenize import BlanklineTokenizer

nltk.download('punkt')

def getParagraphs(text):
    para = text.split("\n\n")
