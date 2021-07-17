import re
from constants import Consts


neg = {}
pos = {}
neg_bi = {}
pos_bi = {}
num_of_pos = 0
num_of_neg = 0


def pre_process_filter(line: str) -> list[str]:
    for word in re.split('[\W\s]', line):
        if word != '':
            yield word


def cleanse_bigram(bigram: dict):


def read_training_datasets():
    # Reading Negative Dataset
    with open(Consts.NEGATIVE_DATASET, 'r') as file:
        for line in file:
            prev_word = ''
            for word in pre_process_filter(line):
                neg[word] = neg.get(word, 0) + 1
                if word not in neg_bi:
                    neg_bi[word] = {}
                neg_bi[word][prev_word] = neg_bi[word].get(prev_word, 0) + 1
                prev_word = word

    # Reading Positive Dataset
    with open(Consts.POSITIVE_DATASET, 'r') as file:
        for line in file:
            prev_word = ''
            for word in pre_process_filter(line):
                pos[word] = pos.get(word, 0) + 1
                if word not in pos_bi:
                    pos_bi[word] = {}
                pos_bi[word][prev_word] = pos_bi[word].get(prev_word, 0) + 1
                prev_word = word

    # Removing very low or very high frequent words
    cleanse_unigram(neg)
    cleanse_unigram(pos)
    cleanse_bigram(neg_bi)
    cleanse_bigram(pos_bi)

    # Counting number of negative and positive words
    global num_of_neg, num_of_pos
    num_of_neg = count_unigram(neg)
    num_of_pos = count_unigram(pos)


def main():
    read_training_datasets()
    for i in neg_bi:
        print(i, neg_bi[i])


if __name__ == '__main__':
    main()
