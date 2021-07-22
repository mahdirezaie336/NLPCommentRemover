class Consts:

    # dataset files address
    NEGATIVE_DATASET = './rt-polarity.neg'
    POSITIVE_DATASET = './rt-polarity.pos'

    # Bond limits
    LOWER_FREQUENCY_CUTOFF = 2
    UPPER_FREQUENCY_CUTOFF = 5

    # Main settings
    TEST_SET_PERCENTAGE = 0.1
    USE_LOGARITHM = True

    # Lambdas for bigram model
    EPSILON = 0.1
    LAMBDA_1 = 0.7
    LAMBDA_2 = 0.2
    LAMBDA_3 = 0.1

    # Lambdas for unigram model
    EPSILON_1 = 0.1
    LAMBDA_1_1 = 0.8
    LAMBDA_1_2 = 0.2
