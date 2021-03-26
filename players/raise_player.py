from leduc.players.player import Player
import numpy as np


class RaisePlayer(Player):

    def select_action(self, valid_actions, state):
        # if '2R' in valid_actions:
        #     return '2R'
        # elif '4R' in valid_actions:
        #     return '4R'
        # else:
        #     return np.random.choice(valid_actions)
        #
        validactions = state.valid_actions()
        if (self.mycard.rank > 12):
            print("raise player current rank is:", self.mycard.rank, ">12, so Raise")
            if '2R' in validactions:
                action = '2R'
            elif '4R' in validactions:
                action = '4R'
            else:
                action = 'C'
        else:
            action = 'F'

        return action