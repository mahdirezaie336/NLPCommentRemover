from constants import Consts


class UnigramModel:
    __dict: dict[str: int]

    def __init__(self):
        self.__dict = {}
        self.__size = 0

    def __getitem__(self, item):
        if item not in self.__dict:
            self.__dict[item] = 0
        return self.__dict[item]

    def __setitem__(self, key, value):
        self.__size += value
        if key in self.__dict:
            self.__size -= self.__dict[key]
        self.__dict[key] = value

    def __len__(self):
        return self.__size

    def __str__(self):
        return str(self.__dict)

    def __repr__(self):
        return str(self)

    def __contains__(self, item):
        return item in self.__dict

    def remove_word(self, item):
        self.__size -= len(self.__dict[item])
        del self.__dict[item]

    def add_word(self, item):
        self[item] += 1
        self.__size += 1

    def get_probability_of(self, word):
        if self.__size == 0:
            return 0.0
        return self.__dict.get(word, 0) / self.__size

    def clean(self, min_number_of_repeats, top_n_maximums):
        to_remove = []

        # Remove words with number of repeats less than threshold
        for word in self.__dict:
            if self.__dict[word] <= min_number_of_repeats:
                to_remove.append(word)
        for i in to_remove:
            self.__size -= self.__dict[i]
            del self.__dict[i]

        # Remove top n repeated words
        for i in range(top_n_maximums):
            maximum = 0
            max_word = ''
            for word in self.__dict:
                if self.__dict[word] > maximum:
                    maximum = self.__dict[word]
                    max_word = word
            if max_word != '':
                self.__size -= self.__dict[max_word]
                del self.__dict[max_word]


class BigramModel:
    __dict: dict[str: dict[str: int]]
    __unigrams: UnigramModel

    def __init__(self, unigrams):
        self.__dict = {}
        self.__size = 0
        self.__unigrams = unigrams

    def __getitem__(self, item: tuple):
        if item[0] not in self.__dict:
            self.__dict[item[0]] = {}
        if item[1] not in self.__dict[item[0]]:
            self.__dict[item[0]][item[1]] = 0
        return self.__dict[item[0]][item[1]]

    def __setitem__(self, key: tuple, value):
        self.__size += value
        if key[0] not in self.__dict:
            self.__dict[key[0]] = {}
        elif key[1] in self.__dict[key[0]]:
            self.__size -= self.__dict[key[0]][key[1]]
        self.__dict[key[0]][key[1]] = value

    def __len__(self):
        return self.__size

    def __str__(self):
        return str(self.__dict)

    def __repr__(self):
        return str(self)

    def get_unigrams(self):
        return self.__unigrams

    def word2_if_word1(self, word1, word2):
        if word1 not in self.__unigrams:
            return 0.0
        return self[word1, word2] / self.__unigrams[word1]

    def clean(self, min_number_of_repeats, top_n_maximums):
        to_remove = []

        # Remove words with number of repeats less than threshold
        for first_word in self.__dict:
            for second_word in self.__dict[first_word]:
                if self.__dict[first_word][second_word] <= min_number_of_repeats:
                    to_remove.append((first_word, second_word))
        for i in to_remove:
            del self.__dict[i[0]][i[1]]
            self.__size -= 1
            if len(self.__dict[i[0]]) == 0:
                del self.__dict[i[0]]

        # Remove top n repeated words
        for i in range(top_n_maximums):
            maximum = 0
            max_word = ('', '')
            for first_word in self.__dict:
                for second_word in self.__dict[first_word]:
                    if self.__dict[first_word][second_word] > maximum:
                        maximum = self.__dict[first_word][second_word]
                        max_word = (first_word, second_word)
            if max_word != ('', ''):
                self.__size -= 1
                del self.__dict[max_word[0]][max_word[1]]
            if len(self.__dict.get(max_word[0], '1')) == 0:
                del self.__dict[max_word[0]]

    def get_probability_of_two(self, word1, word2):
        p1 = Consts.LAMBDA_1 * self.word2_if_word1(word1, word2)
        p2 = Consts.LAMBDA_2 * self.__unigrams.get_probability_of(word2)
        p3 = Consts.LAMBDA_3 * Consts.EPSILON
        return p1 + p2 + p3

    def get_probability_of_sentence(self, sentence: list[str]):
        mul = self.__unigrams.get_probability_of(sentence[0])
        for i in range(1, len(sentence)):
            mul *= self.get_probability_of_two(sentence[i-1], sentence[i])
        return mul
