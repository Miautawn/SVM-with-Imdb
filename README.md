# What is this?
A python project that tries to predict movie genre with from its description SVM model.

## How it works:
1) The dataset is pulled from http://www.cs.cmu.edu/~ark/personas/
2) The data is cleaned and vectorized with TF-IDF
3) The SVM will try to predict the film genre

![1](https://user-images.githubusercontent.com/24988290/114315228-a842ef00-9b06-11eb-9c66-7b169852c800.PNG)
![2](https://user-images.githubusercontent.com/24988290/114315230-a9741c00-9b06-11eb-8472-3e5bb6ff1c9c.PNG)
![3](https://user-images.githubusercontent.com/24988290/114315232-aa0cb280-9b06-11eb-9436-c8d82404b337.PNG)

## How to run it:
1) download `plot_summaries.txt` and `movie_metadata.tsv` files, place them both into "data" folder 
2) install dependencies using pipenv:
```shell
>> pipenv install --ignore-pipfile
```
4) Run dataExtraction.py in order to extract clean data
5) Run SVM.py to train and run the model, it will print out accuracy and will ask you to input sentences for further classification
