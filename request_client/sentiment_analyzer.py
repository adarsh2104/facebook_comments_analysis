import re
from typing_extensions import Literal
import unicodedata
from statistics import mean
import inflect
import nltk
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# from .models import PostComments

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')


def remove_non_ascii(words):
    """Remove non-ASCII character from List of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode(
            'ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)
    return new_words
# To LowerCase
def to_lowercase(words):
    """Convert all characters to lowercase from List of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words
# Remove Punctuation , then Re-Plot Frequency Graph
def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words
# Replace Numbers with Textual Representations
def replace_numbers(words):
    """Replace all interger occurrences in list of tokenized words with textual representation"""
    p = inflect.engine()
    new_words = []
    for word in words:
        if word.isdigit():
            new_word = p.number_to_words(word)
            new_words.append(new_word)
        else:
            new_words.append(word)
    return new_words
# Remove Stopwords
def remove_stopwords(words):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in stopwords.words('english'):
            new_words.append(word)
    return new_words
# Combine all functions into Normalize() function
def normalize(words):
    words = remove_non_ascii(words)
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = replace_numbers(words)
    words = remove_stopwords(words)
    return words

def review_type(compound_scores:list=[0]) -> Literal['Positive','Negative']:
    return 'Positive' if mean(compound_scores) > 0 else 'Negative'
    



def main(comment_lst:list=[]):
    review = None
    nested_sent_token = [nltk.sent_tokenize(lst) for lst in comment_lst]
    flat_sent_token = [item for sublist in nested_sent_token for item in sublist]
    sents = normalize(flat_sent_token)
    sid = SentimentIntensityAnalyzer()
    sentiment = []
    compound_scores = []
    for sent in sents:
        if len(sent) > 35:
            sent_scores = sid.polarity_scores(sent)
            compound_scores.append(sent_scores['compound'])
            sentiment.append({'comment':sent,**sent_scores})
    
    if len(compound_scores) > 0:
        review = review_type(compound_scores)
    
    return sentiment,review

