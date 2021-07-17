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


class BigramModel:
    __dict: dict[str: dict[str: int]]

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

    def word2_if_word1(self, word1, word2):
        if word1 not in self.__unigrams:
            return 0.0
        return self[word1, word2] / self.__unigrams[word1]

