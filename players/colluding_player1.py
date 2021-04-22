from leduc.players.player import Player
import numpy as np

#copy every action of a given Player

class ColludePlayer(Player):
    def leader_action(self, validactions, cards, players, leaderID, victimID,state):
        leader_card=players[state.colludLeader].mycard.rank
        follower_card=players[state.colludFollower].mycard.rank
        #print("leader and follower cards:",leader_card,follower_card)

        #print("current player:",self.name)
        board_card=state.cards[len(players)].rank
        print("board card:",board_card)

        is_pair=False
        if leader_card==board_card or follower_card==board_card:
            is_pair=True
            print("pair happenned...")

        # if is_pair==True:
        #     if self.mycard.rank!=board_card:
        #         return 'F'  #Other collusive player has sure win so fold.
        # if leader_card>=follower_card and follower_card !=board_card:   #follower is not equal to board and smaller card
        #     if self.name=='follower':
        #         print("leader has follower equal or higher card, follower is not eqaul board, let leader play")
        #         return 'F'

        if (leader_card > 13 or follower_card>13 or is_pair==True):
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
            action = 'F'

        return action

    def follower_action(self, valid_actions, cards, players, leaderID,state):
        if players[leaderID].played_current_round == 1:
            print("collusion: copy leaders action...")
            action = players[leaderID].last_action
        else:
            action = 'F'

        return action