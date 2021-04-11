import re
from bs4 import BeautifulSoup
from tqdm import tqdm
import nltk
from nltk.corpus import stopwords

stoplist = set(stopwords.words('english'))

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)

    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase


def cleanData(data):
    preprocessed_sentences = []
    for sentence in tqdm(data):
        sentence = re.sub(r"http\S+", "", sentence)   # Remove URL's from text
        sentence = BeautifulSoup(sentence, 'lxml').get_text()  # Clean HTML tags
        sentence = decontracted(sentence)  # to remove shortening of words
        sentence = re.sub("\S*\d\S*", "", sentence).strip()  # remove words with numbers
        sentence = re.sub('[^A-Za-z]+', ' ', sentence)  # Remove special characters
        splitted = sentence.split()
        sentence = ' '.join(e.lower() for e in sentence.split() if e.lower() not in stoplist)  #Experiment with this
        # Turn into lower case and join into a sentence if a word is not a stopword
        # I do not apply stemming for better results, i don't know why
        preprocessed_sentences.append(sentence.strip())
    return preprocessed_sentences