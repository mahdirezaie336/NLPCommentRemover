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


def count_unigram(unigram: dict):
    return sum(unigram.values())


def probability(w, unigram: dict, unigram_length: int):
    return unigram[w] / unigram_length


def conditional_probability(w1, w2, bigram: dict, unigram: dict):
    if unigram[w2] > 0:
        return bigram[w1][w2] / unigram[w2]
    return 0.0


def cleanse_unigram(unigram: dict):
    to_remove = []

    # Remove words with number of repeats less than threshold
    for word in unigram:
        if unigram[word] <= Consts.LOWER_FREQUENCY_CUTOFF:
            to_remove.append(word)
    for i in to_remove:
        del unigram[i]

    # Remove top n repeated words
    for i in range(Consts.UPPER_FREQUENCY_CUTOFF):
        maximum = 0
        max_word = ''
        for word in unigram:
            if unigram[word] > maximum:
                maximum = unigram[word]
                max_word = word
        del unigram[max_word]


def cleanse_bigram(bigram: dict):
    to_remove = []

    # Remove words with number of repeats less than threshold
    for first_word in bigram:
        for second_word in bigram[first_word]:
            if bigram[first_word][second_word] <= Consts.LOWER_FREQUENCY_CUTOFF:
                to_remove.append((first_word, second_word))
    for i in to_remove:
        del bigram[i[0]][i[1]]
        if len(bigram[i[0]]) == 0:
            del bigram[i[0]]

    # Remove top n repeated words
    for i in range(Consts.UPPER_FREQUENCY_CUTOFF):
        maximum = 0
        max_word = ('', '')
        for first_word in bigram:
            for second_word in bigram[first_word]:
                if bigram[first_word][second_word] > maximum:
                    maximum = bigram[first_word][second_word]
                    max_word = (first_word, second_word)
        del bigram[max_word[0]][max_word[1]]
        if len(bigram[max_word[0]]) == 0:
            del bigram[max_word[0]]


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
