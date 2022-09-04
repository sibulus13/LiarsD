from Dices import Dices


class Player:
    def __init__(self, name = '', score = 0, num_dices = 5, is_player = False) -> None:
        self.name = name
        self.score = score
        self.num_dices = num_dices
        self.dices = Dices(num_dices)
        self.is_player = is_player
        
    def change_name(self, name):
        self.name = name
        
    def change_score(self, score):
        self.score = score
        
    def change_num_dice(self, num_dice):
        self.num_dice = num_dice
    
    def roll(self):
        self.dices.roll()
        
    def show_player_info(self):
        print(f'name: {self.name}\t score: {self.score} \t num_dice: {self.num_dices} \t isPlayer:{self.is_player}')

        # self.dices.show()

        
if __name__ == '__main__':
    p1 = Player()
    p1.show_player_info()