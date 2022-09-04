from tempfile import gettempdir
from unicodedata import name
import random
from unittest.mock import DEFAULT

DEFAULT_POSSIBLE_ROLLS = range(1, 7)


class Dices:
    def __init__(self, num_dice=5, DEFAULT_POSSIBLE_ROLLS=DEFAULT_POSSIBLE_ROLLS) -> None:
        self.num_dice = num_dice
        self.POSSIBLE_ROLLS = DEFAULT_POSSIBLE_ROLLS
        self.__dices = random.sample(self.POSSIBLE_ROLLS, self.num_dice)

    def roll(self):
        '''roll dices'''
        rolls = random.sample(self.POSSIBLE_ROLLS, self.num_dice)
        # print('rolled', rolls)
        self.__dices = rolls

    def show(self):
        '''Show rolls'''
        print(self.__dices)
        return self.__dices

    def get(self):
        return self.__dices
    

    def change_num_dices(self, new_num_dice):
        self.num_dice = new_num_dice


if __name__ == '__main__':
    INITIAL_DICE_COUNT = 5
    p1 = Dices(INITIAL_DICE_COUNT)

    p1.roll()
    p1.show()
