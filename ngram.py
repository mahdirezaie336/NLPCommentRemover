class UnigramModel:

    __dict: dict[str: int]

    def __init__(self):
        self.__dict = {}
        self.__size = 0

    def __getitem__(self, item):
        return self.__dict.get(item, 0)

    def __setitem__(self, key, value):
        self.__size += value
        if key in self.__dict:
             self.__size -= self.__dict[key]
        self.__dict[key] = value

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
        return self.__dict.get(item, UnigramModel())

    def __setitem__(self, key, value):
        self.__dict[key] = value
