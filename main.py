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
    use_logarithm = Consts.USE_LOGARITHM
    negative_probability = neg.get_probability_of_sentence(sentence, use_logarithm=use_logarithm)
    positive_probability = pos.get_probability_of_sentence(sentence, use_logarithm=use_logarithm)
    if negative_probability > positive_probability:
        return neg
    return pos


def test_bigram_model(neg_bi: BigramModel, neg_test: list[list[str]], pos_bi: BigramModel):

    # Initializing parameters with 0
    max_precision = 0
    max_l1 = 0
    max_l2 = 0
    max_e = 0
    NUMBER = 10

    # Searching all possible values
    for lambda1 in range(NUMBER):
        for lambda2 in range(NUMBER):
            for epsilon in range(1, NUMBER):
                print(lambda1, lambda2, epsilon)

                # Setting parameters
                Consts.LAMBDA_1 = lambda1 / NUMBER
                Consts.LAMBDA_2 = lambda2 / NUMBER
                Consts.LAMBDA_3 = 1 - (Consts.LAMBDA_2 + Consts.LAMBDA_1)
                Consts.EPSILON = epsilon / NUMBER

                # Counting number of correct and wrong classifications
                correct_count = 0
                wrong_count = 0
                if (lambda1 + lambda2)/NUMBER < 1:
                    for sentence in neg_test:
                        if neg_bi == find_class(neg_bi, pos_bi, sentence):
                            correct_count += 1
                        else:
                            wrong_count += 1
                else:
                    # If sum of l1 and l2 is more than 1
                    wrong_count += 1
                print(correct_count, wrong_count)
                # Finding maximum
                precision = correct_count / (correct_count + wrong_count)
                if precision > max_precision:
                    max_precision = precision
                    max_l1 = lambda1
                    max_l2 = lambda2
                    max_e = epsilon

    return max_l1/NUMBER, max_l2/NUMBER, max_e, max_precision


def main():
    neg, neg_bi, neg_test, pos, pos_bi, pos_test = read_training_datasets()
    print('here')
    print(test_bigram_model(neg_bi, neg_test, pos_bi))
    return
    try:
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
