import re
from ngram import *
import sys
import random
import numpy as np


def pre_process_filter(line: str) -> list[str]:
    for word in re.split('[\W\s]', line):
        if word != '':
            yield word.lower()


def read_training_datasets() -> (UnigramModel, BigramModel, list, UnigramModel, BigramModel, list):

    def create_models(dataset_file_address) -> (UnigramModel, BigramModel, list[list[str]]):
        uni = UnigramModel()
        bi = BigramModel(uni)
        test = []                                                       # List of test dataset
        # Reading Negative Dataset
        with open(dataset_file_address, 'r') as file:
            for line in file:
                for part in re.split('[.]', line):
                    use_for_test = random.random() < Consts.TEST_SET_PERCENTAGE
                    sentence_list = []
                    prev_word = ''
                    for word in pre_process_filter(part):
                        if use_for_test:
                            sentence_list.append(word)
                        else:
                            uni[word] += 1
                            bi[prev_word, word] += 1
                            prev_word = word
                    if use_for_test and len(sentence_list) > 0:
                        test.append(sentence_list)
        return uni, bi, test

    neg, neg_bi, neg_test = create_models(Consts.NEGATIVE_DATASET)
    pos, pos_bi, pos_test = create_models(Consts.POSITIVE_DATASET)

    # Removing very low or very high frequent words
    pos.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    neg.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    pos_bi.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)
    neg_bi.clean(Consts.LOWER_FREQUENCY_CUTOFF, Consts.UPPER_FREQUENCY_CUTOFF)

    return neg, neg_bi, neg_test, pos, pos_bi, pos_test


def find_class(neg, pos, sentence: list[str]):
    use_logarithm = Consts.USE_LOGARITHM
    negative_probability = neg.get_probability_of_sentence(sentence, use_logarithm=use_logarithm)
    positive_probability = pos.get_probability_of_sentence(sentence, use_logarithm=use_logarithm)
    if negative_probability > positive_probability:
        return neg
    return pos


def test_bigram_model(neg_bi: BigramModel, neg_test: list[list[str]], pos_bi: BigramModel):
    random.shuffle(neg_test)
    # Initializing parameters with 0
    max_precision = 0
    max_l1 = 0
    max_l2 = 0
    max_e = 0
    step = 0.1

    # Searching all possible values
    for lambda1 in np.arange(0, 1, step):
        for lambda2 in np.arange(0, 1, step):
            for epsilon in np.arange(0.1, 1, step):
                # print(lambda1, lambda2, epsilon)

                # Setting parameters
                Consts.LAMBDA_1 = lambda1
                Consts.LAMBDA_2 = lambda2
                Consts.LAMBDA_3 = 1 - (lambda1 + lambda2)
                Consts.EPSILON = epsilon

                # Counting number of correct and wrong classifications
                correct_count = 0
                wrong_count = 0
                if (lambda1 + lambda2) < 1:
                    for sentence in neg_test:
                        if neg_bi == find_class(neg_bi, pos_bi, sentence):
                            correct_count += 1
                        else:
                            wrong_count += 1
                else:
                    # If sum of l1 and l2 is more than 1
                    wrong_count += 1
                # print(correct_count, wrong_count)
                # Finding maximum
                precision = correct_count / (correct_count + wrong_count)
                if precision > max_precision:
                    max_precision = precision
                    max_l1 = lambda1
                    max_l2 = lambda2
                    max_e = epsilon

    return max_l1, max_l2, max_e, max_precision


def test_unigram_model(neg: UnigramModel, neg_test: list[list[str]], pos: UnigramModel):
    random.shuffle(neg_test)

    # Initializing parameters with 0
    max_precision = 0
    max_l1 = 0
    max_l2 = 0
    max_e = 0
    step = 0.1

    # Searching all possible values
    for lambda1 in np.arange(0, 1, step):
        for epsilon in np.arange(0.1, 1, step):
            # print(lambda1, lambda2, epsilon)

            # Setting parameters
            Consts.LAMBDA_1_1 = lambda1
            Consts.LAMBDA_1_2 = 1 - lambda1
            Consts.EPSILON = epsilon

            # Counting number of correct and wrong classifications
            correct_count = 0
            wrong_count = 0
            for sentence in neg_test:
                if neg == find_class(neg, pos, sentence):
                    correct_count += 1
                else:
                    wrong_count += 1

            # Calculating precision
            if (correct_count + wrong_count) > 0:
                precision = correct_count / (correct_count + wrong_count)
            else:
                precision = 0

            if precision > max_precision:
                max_precision = precision
                max_l1 = lambda1
                max_l2 = 1 - lambda1
                max_e = epsilon

    return max_l1, max_l2, max_e, max_precision


def main():

    try:
        neg, neg_bi, neg_test, pos, pos_bi, pos_test = read_training_datasets()

        # Testing bigram dataset and set parameters
        l1, l2, e, _ = test_bigram_model(pos_bi, pos_test, neg_bi)
        print('Found', l1, 'for LAMBDA 1 and', l2, 'for LAMBDA 2 and', e, 'for epsilon.')
        Consts.LAMBDA_1 = l1
        Consts.LAMBDA_2 = l2
        Consts.LAMBDA_3 = 1 - l1 - l2
        Consts.EPSILON = e

        # Testing unigram dataset and set parameters
        l1, l2, e1, _ = test_unigram_model(pos, pos_test, neg)
        Consts.LAMBDA_1 = l1
        Consts.LAMBDA_2 = l2
        Consts.EPSILON_1 = e1

        # Getting from user
        input_str = input('Choose one of models:\n\n1- Unigram model\n2- Bigram model\n')
        is_unigram = input_str.startswith('1')

        # Getting inputs loop
        while True:
            input_str = input('Enter an opinion: ')
            if input_str == '!q':
                break
            input_list = [i for i in pre_process_filter(input_str)]


            if True:
                print('\nfilter this\n')
            else:
                print('\nnot filter this\n')

    except KeyboardInterrupt:
        print('\nExiting due to a keyboard interrupt...', file=sys.stderr)
    else:
        print('\nExiting ...')


if __name__ == '__main__':
    main()
