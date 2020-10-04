import csv
import pandas as pd
import json
from tqdm import tqdm

"""
reading plot details
"""
meta_data = pd.read_csv("./data/movie.metadata.tsv", sep='\t')
meta_data.columns = ["movie_id", 1,2,3,4,5,6,7,"genre"]
meta_data["movie_id"] = meta_data["movie_id"].astype(str) #converting movie id into string

"""
reading meta-data details
"""
plot_data = []
with open("./data/plot_summaries.txt", 'r', encoding="utf8") as f:
    reader = csv.reader(f, dialect='excel-tab')
    for row in tqdm(reader):
        plot_data.append(row)

movie_id = []
movie_plot = []

for movie in tqdm(plot_data):
    movie_id.append(movie[0])
    movie_plot.append(movie[1])

"""
merging meta-data and plot
"""
data = pd.DataFrame({"movie_id": movie_id, "plot":movie_plot})
data = pd.merge(data, meta_data[["movie_id", "genre"]], on="movie_id")

genres = []
for dict in tqdm(data["genre"]):
    genres.append(list(json.loads(dict).values()))


"""
Deleting points with no genre tags and selecting only ones from the specified list
"""

data["genre"] = genres
data = data[data["genre"].str.len() != 0]

genres = []
for list in data["genre"]:
    check = False
    for item in list:
        if item in ["Drama", "Horror", "Action", "Science Fiction", "Comedy", "Thriller"]:  #Specified list
            genres.append(item)
            check = True
            break
    if not check:
        genres.append("null")


data["genre"] = genres
data = data[data["genre"] != "null"]
data = data.drop(["movie_id"], axis=1)

import re
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
stoplist = stopwords.words("english")

"""
Text cleaning
"""

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

preprocessed_sentences= []

for sentence in tqdm(data["plot"]):
    sentence = re.sub(r"http\S+", "", sentence)   # Remove URL's from text
    sentence = BeautifulSoup(sentence, 'lxml').get_text()  # Clean HTML tags
    sentence = decontracted(sentence)  # to remove shortening of words
    sentence = re.sub("\S*\d\S*", "", sentence).strip()  # remove words with numbers
    sentence = re.sub('[^A-Za-z]+', ' ', sentence)  # Remove special characters
    sentence = ' '.join(e.lower() for e in sentence.split() if e.lower() not in stoplist)  #Experiment with this
    # Turn into lower case and join into a sentence if a word is not a stopword
    # I do not apply stemming for better results, i don't know why
    preprocessed_sentences.append(sentence.strip())

data["plot"] = preprocessed_sentences

"""
Exporting clean dataset
"""
data.to_csv("./data/realData.csv", index=False)