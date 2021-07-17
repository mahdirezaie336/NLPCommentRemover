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

    def remove_word(self, item):
        self.__size -= len(self.__dict[item])
        del self.__dict[item]

    def add_word(self, item):
        self[item] += 1
        self.__size += 1


class BigramModel:
    __dict: dict[str: UnigramModel]

    def __init__(self):
        self.__dict = {}
        self.__size = 0

    def __getitem__(self, item):
        if item not in self.__dict:
            self.__dict[item] = UnigramModel()
        return self.__dict[item]

    def __setitem__(self, key, value):
        print('Set item called in bigram')
        self.__size += len(value)
        if key in self.__dict:
            self.__size -= len(self.__dict[key])
        self.__dict[key] = value

    def __len__(self):
        return sum([len(self.__dict[i]) for i in self.__dict])

    def __str__(self):
        return str(self.__dict)

    def __repr__(self):
        return str(self)


b = BigramModel()
b['2']['1'] += 5
print(len(b))
