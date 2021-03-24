from leduc.players.player import Player
import numpy as np


class RandomPlayer(Player):

    def select_action(self, valid_actions, current_state):
        return np.random.choice(valid_actions)
