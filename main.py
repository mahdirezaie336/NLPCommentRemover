import re
from ngram import *
import sys
import random


def pre_process_filter(line: str) -> list[str]:
    for word in re.split('[\W\s]', line):
        if word != '':
            yield word.lower()


def read_training_datasets() -> (UnigramModel, BigramModel, list, UnigramModel, BigramModel, list):
    neg = UnigramModel()
    neg_bi = BigramModel(neg)
    neg_test = []                                                       # List of test dataset
    # Reading Negative Dataset
    with open(Consts.NEGATIVE_DATASET, 'r') as file:
        for line in file:
            use_for_test = random.random() < Consts.TEST_SET_PERCENTAGE
            sentence_list = []
            prev_word = ''
            for word in pre_process_filter(line):
                if use_for_test:
                    sentence_list.append(word)
                else:
                    neg[word] += 1
                    neg_bi[prev_word, word] += 1
                    prev_word = word
            if use_for_test:
                neg_test.append(sentence_list)

    pos = UnigramModel()
    pos_bi = BigramModel(neg)
    pos_test = []                                                       # List of test dataset
    # Reading Positive Dataset
    with open(Consts.POSITIVE_DATASET, 'r') as file:
        for line in file:
            use_for_test = random.random() < Consts.TEST_SET_PERCENTAGE
            sentence_list = []
            prev_word = ''
            for word in pre_process_filter(line):
                if use_for_test:
                    sentence_list.append(word)
                else:
                    pos[word] += 1
                    pos_bi[prev_word, word] += 1
                    prev_word = word
            if use_for_test:
                pos_test.append(sentence_list)

    # Removing very low or very high frequent words
    pos.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    neg.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    pos_bi.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    neg_bi.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)

    return neg, neg_bi, neg_test, pos, pos_bi, pos_test


def find_class(neg, pos, sentence: list[str]):
    # Getting probability
    use_logarithm = Consts.USE_LOGARITHM
    negative_probability = neg.get_probability_of_sentence(sentence, use_logarithm=use_logarithm)
    positive_probability = pos.get_probability_of_sentence(sentence, use_logarithm=use_logarithm)
    if negative_probability > positive_probability:
        return neg
    return pos


def main():
    neg, neg_bi, neg_test, pos, pos_bi, pos_test = read_training_datasets()
    try:
        input_str = input('Choose one of models:\n\n1- Unigram model\n2- Bigram model\n')
        is_unigram = input_str.startswith('1')

        # Getting inputs loop
        while True:
            input_str = input('Enter an opinion: ')
            if input_str == '!q':
                break
            input_list = [i for i in pre_process_filter(input_str)]



            # Showing results
            print('negative probability: ', negative_probability)
            print('positive probability: ', positive_probability)
            if negative_probability > positive_probability:
                print('\nfilter this\n')
            else:
                print('\nnot filter this\n')

    except KeyboardInterrupt:
        print('\nExiting due to a keyboard interrupt...', file=sys.stderr)
    else:
        print('\nExiting ...')


if __name__ == '__main__':
    main()
