from Player import Player


class Room:
    '''Room'''

    def __init__(self, MAX_NUM_PLAYERS):
        '''Starting a game room, room size is declared'''
        self.MAX_NUM_PLAYERS = MAX_NUM_PLAYERS
        self.num_players = 0
        self.players = []
        self.max_dice_count = 0
        print(f'Created room for max {MAX_NUM_PLAYERS} players')       
        
    def roll(self):
        if self.num_players == 0:
            print('No players, cannot roll')
            return
        for player in self.players:
            player.roll()
        

    def show_dices(self):
        all_dices = []
        if self.num_players == 0:
            print('No players, cannot roll')
            return []

        for player in self.players:
            all_dices = all_dices + player.dices.show()
        return all_dices

    def get_dices(self):
        all_dices = []
        if self.num_players == 0:
            print('No players, cannot roll')
            return []

        for player in self.players:
            all_dices = all_dices + player.dices.get()
        return all_dices
            
    def index_OOB(self, player_index):
        if player_index > self.num_players:
            print('player index out of bound')
            return True
        return False


    def change_player_name(self, new_name, player_index):
        if self.index_OOB(player_index):
            return
        
        self.players[player_index].name = new_name

    def add_player(self, new_name, is_player=False):
        if self.num_players+1 > self.MAX_NUM_PLAYERS:
            print('Room is full')
            return
        self.num_players = self.num_players + 1
        self.players.append(Player(name=new_name, is_player=is_player))
        self.max_dice_count = self.get_dice_count()
        # self.show_state()

    def delete_player(self, player_index):
        if self.num_players - 1 < 0:
            print('No more players left in the room')
            return
        if self.index_OOB(player_index):
            return
        self.num_players = self.num_players - 1
        self.players.pop(player_index)
        self.max_dice_count = self.get_dice_count()
        # self.show_state()
        
    def get_player_names(self):
        names = []
        for player in self.players:
            names.append(player.name)
        return names

    def show_state(self):
        # print(self)
        print(f'num_players: {self.num_players}')
        for player in self.players:
            player.show_player_info()
        for player in self.players:
            player.dices.show()
        print()
        
    def get_dice_count(self):
        num_dices = 0
        for player in self.players:
            num_dices = num_dices + player.num_dices
        # print('total dice count:', num_dices)
        return num_dices


if __name__ == '__main__':
    MAX_NUM_PLAYERS = 3
    room = Room(3)
    # room.show_state()
    # room.show_dices()
    # room.delete_player(0)
    # room.delete_player(1)
    # room.show_state()
    # room.add_player('Michael', True)
    # room.add_player('bot1', False)
    # room.add_player('bot2', False)
    # room.add_player('bot3', False)
    # room.show_state()
    # room.delete_player(0)
    # room.delete_player(1)
    # room.show_state()