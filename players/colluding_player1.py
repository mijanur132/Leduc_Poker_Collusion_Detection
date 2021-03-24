from leduc.players.player import Player
import numpy as np

#copy every action of a given Player

class ColludePlayer(Player):
    def leader_action(self, valid_actions, cards, players, leaderID, victimID,state):
        validactions = state.valid_actions()
        if self.mycard.rank > 12:
            print("current rank is:", self.mycard.rank, ">12, so Raise")
            print("victims last action:", players[victimID].last_action)
            if players[victimID].last_action == 'F':
                print('victim folded: dont raise-->')
                action = 'C'
            else:
                if '2R' in validactions:
                    action = '2R'
                elif '4R' in validactions:
                    action = '4R'
                else:
                    action = 'C'
        else:
            action = 'C'

        return action

    def follower_action(self, valid_actions, cards, players, leaderID,state):
        if players[leaderID].played_current_round == 1:
            print("collusion: copy leaders action...")
            action = players[leaderID].last_action
        else:
            action = 'C'

        return action