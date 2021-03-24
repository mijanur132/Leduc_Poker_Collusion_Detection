from leduc.players.player import Player
import numpy as np


class FoldPlayer(Player):

    def select_action(self, valid_actions, current_state):
        if 'F' in valid_actions:
            return 'F'
        else:
            return np.random.choice(valid_actions)
