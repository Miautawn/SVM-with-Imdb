# What is this?
A python project that tries to predict movie genre with from its description SVM model.

## How it works:
1) The dataset is pulled from http://www.cs.cmu.edu/~ark/personas/
2) The data is cleaned and vectorized with TF-IDF
3) The SVM will try to predict the film genre

![image](https://user-images.githubusercontent.com/24988290/97110170-64873500-16e0-11eb-85eb-732fa1015603.png)

## How to run it:
1) download `plot_summaries.txt` and `movie_metadata.tsv` files, place them both into "data" folder 
2) Run dataExtraction.py in order to extract clean data
3) Run SVM.py to train and run the model, it will print out accuracy and will ask you to input sentences for further classification
