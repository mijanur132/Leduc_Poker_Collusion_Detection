from leduc.players.player import Player
import numpy as np


class RaisePlayer(Player):

    def select_action(self, validactions, state):
        cards=state.cards
        print("cards at raise Player:",cards)
        board_card=cards[-1]
        print("board_card",board_card.rank)
        if (self.mycard.rank > 12 or self.mycard.rank==board_card.rank):
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