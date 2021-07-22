# NLP Comment Remover

This project uses basic `Natural Language Processing` techniques to detect bad
and good comments about topic `Artificial Intelligence` and tells you
whether they should be filtered or no.


# Run the Project

To start using this project you need python version >= 3.9.
After installing, simply run the `main.py` file ny then following command:

```
$ python3 main.py
```

On the startup, you will see the following message. Type number of one of options
and press enter to continue.

```
Choose one of models:

1- Unigram model
2- Bigram model

```

Then it starts to test the test dataset and finds the best parameters for language model.
These parameters are some coefficients in calculating probability of being in good
or bad class for a sentence. The results are like this:

```
Testing. Please wait ...
Found 0.2 for LAMBDA 1 and 0.7 for LAMBDA 2 and 0.1 for epsilon.
Precision is 0.6689303904923599 

Enter an opinion: 
```

So the best language model has 67 percent precision here. Now type an opinion.
It will classify the opinion and tells you that this comment should be filtered
or no. Here are some examples:

```
Enter an opinion: the movie is tedious

filter this

Enter an opinion: a fascinating piece of art

not filter this
```

