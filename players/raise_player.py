from leduc.players.player import Player
import numpy as np


class RaisePlayer(Player):

    def select_action(self, valid_actions, current_state):
        if '2R' in valid_actions:
            return '2R'
        elif '4R' in valid_actions:
            return '4R'
        else:
            return np.random.choice(valid_actions)
