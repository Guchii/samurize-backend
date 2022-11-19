import nltk
from nltk.tokenize import BlanklineTokenizer

nltk.download('punkt')

def getParagraphs(text):
    return BlanklineTokenizer().tokenize(text)
