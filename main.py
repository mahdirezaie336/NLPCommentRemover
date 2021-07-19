import re
from constants import Consts
from ngram import *


def pre_process_filter(line: str) -> list[str]:
    for word in re.split('[\W\s]', line):
        if word != '':
            yield word.lower()


def read_training_datasets() -> (UnigramModel, BigramModel, UnigramModel, BigramModel):
    neg = UnigramModel()
    neg_bi = BigramModel(neg)
    # Reading Negative Dataset
    with open(Consts.NEGATIVE_DATASET, 'r') as file:
        for line in file:
            prev_word = ''
            for word in pre_process_filter(line):
                neg[word] += 1
                neg_bi[prev_word, word] += 1
                prev_word = word

    pos = UnigramModel()
    pos_bi = BigramModel(neg)
    # Reading Positive Dataset
    with open(Consts.POSITIVE_DATASET, 'r') as file:
        for line in file:
            prev_word = ''
            for word in pre_process_filter(line):
                pos[word] += 1
                pos_bi[word, prev_word] += 1
                prev_word = word

    # Removing very low or very high frequent words
    pos.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    neg.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    pos_bi.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    neg_bi.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)

    return neg, neg_bi, pos, pos_bi


def main():
    neg, neg_bi, pos, pos_bi = read_training_datasets()
    print(neg_bi)
    print(neg_bi.get_unigrams())
    print(neg_bi.word2_if_word1('not', 'working'))


if __name__ == '__main__':
    main()
