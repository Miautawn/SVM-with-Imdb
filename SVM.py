import csv
import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
import numpy as np

data = pd.read_csv("./data/realData.csv")
data["plot"] = data["plot"].astype(str)


new_data = data[data["genre"] == "Drama"][0:6000]
new_data = new_data.append(data[data["genre"] == "Thriller"][:6000])
new_data = new_data.append(data[data["genre"] == "Comedy"][:6000])

# new_data["genre"].value_counts().plot(kind='bar')
# plt.show()
data = new_data
corpus = data["plot"].values

from sklearn.feature_extraction.text import TfidfVectorizer
vect = TfidfVectorizer()
vect.fit(corpus)
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(data["plot"], data["genre"], train_size=0.8, random_state=42)

X_train = vect.transform(X_train)
X_test = vect.transform(X_test)

from sklearn.linear_model import SGDClassifier
classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)
classifier.fit(X_train, Y_train)
print("Score: ", classifier.score(X_test, Y_test))


import helperFunctions
while(True):
    print("please enter a sentence: ")
    generated_text = [input()]
    generated_text = helperFunctions.cleanData(generated_text)
    generated_text = vect.transform(generated_text)
    print(classifier.predict(generated_text))








