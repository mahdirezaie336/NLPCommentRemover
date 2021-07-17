import re

neg = {}
pos = {}
neg_bi = {}
pos_bi = {}
low_frequency_threshold = 2
most_repeated_remove = 5


def pre_process_filter(line: str) -> list[str]:
    for word in re.split('[\W\s]', line):
        if word != '':
            yield word


def cleanse_unigram(unigram: dict):
    to_remove = []

    # Remove words with number of repeats less than threshold
    for word in unigram:
        if unigram[word] <= low_frequency_threshold:
            to_remove.append(word)
    for i in to_remove:
        del unigram[i]

    # Remove top n repeated words
    for i in range(most_repeated_remove):
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
    for word in bigram:
        for word2 in word:
            if bigram[word][word2] <= low_frequency_threshold:
                to_remove.append((word, word2))
    for i in to_remove:
        del bigram[i[0]][i[1]]

    # Remove top n repeated words
    for i in range(most_repeated_remove):
        maximum = 0
        max_word = ('', '')
        for word in bigram:
            for word2 in word:
                if bigram[word][word2] > maximum:
                    maximum = bigram[word][word2]
                    max_word = (word, word2)
        del bigram[max_word[0]][max_word[1]]


def read_training_datasets():
    # Reading Negative Dataset
    with open('./rt-polarity.neg', 'r') as file:
        for line in file:
            prev_word = '<s>'
            for word in pre_process_filter(line):
                neg[word] = neg.get(word, 0) + 1
                if word not in neg_bi:
                    neg_bi[word] = {}
                neg_bi[word][prev_word] = neg_bi[word].get(prev_word, 0) + 1
                prev_word = word

    # Reading Positive Dataset
    with open('./rt-polarity.pos', 'r') as file:
        for line in file:
            prev_word = '<s>'
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


if __name__ == '__main__':
    read_training_datasets()
    for i in neg_bi:
        print(i, neg_bi[i])
