import re


neg = {}
pos = {}


def pre_process_filter(line: str) -> list[str]:
    for word in re.split('[\W\s]', line):
        if word != '':
            yield word


def read_training_datasets():
    # Reading Negative Dataset
    with open('./rt-polarity.neg', 'r') as file:
        for line in file:
            for word in pre_process_filter(line):
                neg[word] = neg.get(word, 0) + 1

    # Reading Positive Dataset
    with open('./rt-polarity.pos', 'r') as file:
        for line in file:
            for word in pre_process_filter(line):
                neg[word] = neg.get(word, 0) + 1


if __name__ == '__main__':
    read_training_datasets()
    for i in neg:
        print(i, neg[i])

