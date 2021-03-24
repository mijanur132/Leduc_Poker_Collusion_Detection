from leduc.players.player import Player
import numpy as np


class CallPlayer(Player):

    def select_action(self, valid_actions, current_state):
        if 'C' in valid_actions:
            return 'C'
        else:
            return np.random.choice(valid_actions)
