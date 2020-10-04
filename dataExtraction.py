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

"""
Text cleaning
"""

import helperFunctions

data["plot"] = helperFunctions.cleanData(data["plot"])


"""
Exporting clean dataset
"""
data.to_csv("./data/realData.csv", index=False)