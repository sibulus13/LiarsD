from Room import Room
import random
import Distribution
from Dices import DEFAULT_POSSIBLE_ROLLS
from Distribution import power_distribution
from liarsD.liarsDPy.scripts.Distribution import calc_dice_likeliness, calc_likeliness_of_claim


'''
For each round:
    go in order to claim
    anyone call call the bluff

for reveal:
    if caller gets it right:
        caller + 1
        bluffer - 0.5
    if wrong:
        caller - 0.5
'''


class Game:
    def __init__(self, MAX_NUM_PLAYERS=2):
        '''Starting a game room, room size is declared'''
        self.room = Room(MAX_NUM_PLAYERS)
        self.last_loser_index = 0
        self.round_num = 0
        self.wild_card_in_play = True
        self.last_claim = {'num': 1, 'face': 0}
        self.VALID_DICE_RANGE = DEFAULT_POSSIBLE_ROLLS

    def match(self, verbose=True):
        '''sequential'''
        print('____Game Started____')
        self.room.roll()
        while True:
            curr_index = self.round_num + self.last_loser_index
            curr_player_index = curr_index % self.room.MAX_NUM_PLAYERS
            curr_player = self.room.players[curr_player_index]
            print('round', self.round_num)
            if self.is_max_claim():
                self.round_result(curr_player_index)
                return
            if curr_player.is_player:
                call, claim = self.player_round()
            else:
                call, claim = self.bot_round_rand()
            if call and self.round_num != 0:
                self.round_result(curr_player_index)
                return
            self.last_claim = claim
            nums = claim['num']
            face = claim['face']
            print(
                f'{curr_player.name} {curr_player_index}:{curr_index} claimed {nums} {face}')
            self.handle_wild_card(claim)
            self.round_num = self.round_num + 1

    def is_max_claim(self):
        '''Checks if the last claim is the largest possible call'''
        LARGEST_NUM_CALLABLE = self.room.max_dice_count
        LARGEST_FACE_CALLABLE = max(self.VALID_DICE_RANGE)
        if self.last_claim['num'] == LARGEST_NUM_CALLABLE and self.last_claim['face'] == LARGEST_FACE_CALLABLE:
            print('max claim reached by last call')
            return True
        return False

    def round_result(self, curr_player_index):
        '''checks if last call is bluff or not and handle scores accordingly'''
        dices = self.room.get_dices()
        print('all_dices', dices)
        num = self.last_claim['num']
        face = self.last_claim['face']
        print(f'player {curr_player_index} called {num} {face}s')
        sum = dices.count(self.last_claim['face'])
        if self.wild_card_in_play:
            sum = sum + dices.count(1)

        if sum >= self.last_claim['num']:
            print(f'Not a bluff, {sum} {face}')
            winner_index = (curr_player_index - 1) % self.room.MAX_NUM_PLAYERS
            loser_index = curr_player_index % self.room.MAX_NUM_PLAYERS
        else:
            print(f'Bluff called, only {sum} {face}')
            loser_index = (curr_player_index - 1) % self.room.MAX_NUM_PLAYERS
            winner_index = curr_player_index % self.room.MAX_NUM_PLAYERS
        self.handle_scores(winner_index, loser_index)
        self.room.show_state()
        self.reset_game()

    def handle_scores(self, winner_index, loser_index):
        '''handles winner and loser score changes'''
        self.room.players[winner_index].score = self.room.players[winner_index].score + 1
        self.room.players[loser_index].score = self.room.players[loser_index].score - 0.5
        self.last_loser_index = loser_index

    def reset_game(self):
        '''reset game state after round conclusion'''
        self.round_num = 0
        self.wild_card_in_play = True
        self.last_claim = {'num': 0, 'face': 0}
        self.VALID_DICE_RANGE = DEFAULT_POSSIBLE_ROLLS
        # self.room.max_dice_count = range(self.room.get_dice_count()+1)

    def handle_wild_card(self, claim):
        if claim['face'] == 1:
            self.wild_card_in_play = False

    def player_round(self):
        claim = {'num': 0, 'face': 0}
        while not self.is_valid_claim(claim):
            user_input = input('Please input your claim as call:0:0, or nocall:3:3. \n Ex: nocall:3:3 implies 3 of 3s\n')
            inputs = user_input.split(':')
            call = True if inputs[0] == 'call' else False
            claim = {'num': int(inputs[1]), 'face': int(inputs[2])}
            if self.round_num != 0 and call == True:
                return True, claim
            if self.round_num == 0 and call == True:
                print("its the first round, you can't call")
                call = False
        return False, claim                
        
    def bot_round_rand(self):
        call = random.choice([True, False])
        claim = {'num': 0, 'face': 0}
        # print(self.last_claim['num'], self.room.max_dice_count)
        possible_nums = range(max(1, self.last_claim['num']), self.room.max_dice_count)
        while not self.is_valid_claim(claim):
            weights = Distribution.power_distribution(len(possible_nums), 3, 1)
            # print(len(possible_nums), len(weights))
            num = random.choices(possible_nums, weights=weights)[0]
            face = random.choice(self.VALID_DICE_RANGE)
            claim = {'num': num, 'face': face}
        return call, claim
    
    
    def bot_round_stat(self):
        # callChance = 1 - calc_likeliness_of_claim()
        
        # claim opportunity
        return
        
        

    def is_valid_claim(self, current_claim):
        VALID_DICE_RANGE = current_claim['face'] in self.VALID_DICE_RANGE
        VALID_NUM_RANGE = current_claim['num'] in range(
            self.room.max_dice_count+1)
        LARGER_NUM_CALLED = current_claim['num'] > self.last_claim['num']
        LARGER_DICE_CALLED = current_claim['face'] > self.last_claim['face']
        # print(current_claim)
        # print(LARGER_NUM_CALLED, LARGER_DICE_CALLED, self.last_claim, current_claim)
        if VALID_DICE_RANGE and VALID_NUM_RANGE and (LARGER_NUM_CALLED or LARGER_DICE_CALLED):
            return True
        return False
    
    def play(self, type = 'dm', num_games = 10):
        types = ['dieth match', 'last die standing']
        match type:
            case 'dm':
                for i in range(num_games):
                    self.match()
            case 'lds':
                return
                
        
if __name__ == '__main__':
    game = Game(3)
    # game.room.add_player('Michael', True)
    game.room.add_player('bot0', False)
    game.room.add_player('bot1', False)
    game.room.add_player('bot2', False)
    # game.room.show_state()
    # for i in range(1):
    #     game.match()
    
    game.play('dm')