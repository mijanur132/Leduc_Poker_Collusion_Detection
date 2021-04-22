from leduc.state import Leduc as State
from leduc.card import Card
from leduc.hand_eval import leduc_eval as eval
from itertools import permutations
from leduc.players.random_player import RandomPlayer
from leduc.players.call_player import CallPlayer
from leduc.players.raise_player import RaisePlayer
from leduc.players.colluding_player1 import ColludePlayer

import random
import numpy as np

'''Leduc Hold'em is a toy poker game sometimes used in academic research (first introduced in Bayes' Bluff: Opponent 
Modeling in Poker). It is played with a deck of six cards, comprising two suits of three ranks each (often the king, 
queen, and jack - in our implementation, the ace, king, and queen). The game begins with each player being dealt one 
card privately, followed by a betting round. Then, another card is dealt face-up as a community (or board) card, and 
there is another betting round. Finally, the players reveal their private cards. If one player's private card is the 
same rank as the board card, he or she wins the game; otherwise, the player whose private card has the higher rank 
wins.'''

'''
Leduc Hold'em is a poker variant where each player is dealt a card from a deck of 3 cards in 2 suits. The first round 
consists of a pre-flop betting round. The second round consists of a post-flop betting round after one board card is 
dealt. There is a two bet maximum per round, with raise sizes of 2 and 4 for each round. Each player antes 1 before 
the game starts.'''


def play_game(players):
    num_cards = len(players) + 1
    cards = [Card(14, 1), Card(13, 1), Card(12, 1), Card(14, 2), Card(13, 2), Card(12, 2)]
    all_combos = [list(t) for t in set(permutations(cards, num_cards))]
    card = np.random.choice(len(all_combos))


    state = State(all_combos[card], len(players), eval, players)
    colludeStarterID=0
    colludeFollowerID=0
    victimID=0
    action=0

    for i in range(0, len(players)):
        players[i].played_current_round = 0
        players[i].mycard=state.cards[i]
        players[i].last_action =0
        #print(i)
        if players[i].collude_starter == 1:  # if current player is colluding palyer
            colludeStarterID=i
            state.colludLeader=i
            print("Collude Starter/Leader ID:",i)
        if players[i].collude_follower == 1:  # if current player is colluding palyer
            colludeFollowerID=i
            state.colludFollower=i
            print("Collude follower ID:",i)
        if players[i].victim == 1:  # if current player is colluding palyer
            victimID=i
            state.victim=i
            print("victim ID:", i)
    # do something

    while state.terminal is False:
        print("Player cards:",state.cards)
        curr_player = state.players[state.turn]
        print('Current Player:----->', curr_player.name)
        if not curr_player.folded:
            curr_player.played_current_round = 1
            if curr_player.collude_starter == 1:
                action=curr_player.leader_action(state.valid_actions(curr_player), cards, players,colludeStarterID, victimID, state)

            if curr_player.collude_follower==1:
                #action = curr_player.follower_action(state.valid_actions(curr_player), cards, players, colludeStarterID, state)
                action = curr_player.leader_action(state.valid_actions(curr_player), cards, players, colludeStarterID,victimID,state)

            if curr_player.collude_starter==0 and curr_player.collude_follower==0:
                action = curr_player.select_action(state.valid_actions(curr_player), state)


            curr_player.last_action=action
            print('Action:', action)
            state = state.take(action)
            for i, player in enumerate(state.players):
                print('pl', player.name, ' bets', player.bets)
        else:
            state.turn += 1



    payout = state.utility()
    print('*' * 50)
    #print('Payout', payout)
    print('Current Amounts', [p.amount for p in players])
    winners = np.argwhere(payout == np.amax(payout)).flatten().tolist()
    # winners
    # print(winners)
    winner_names = []
    if len(winners) > 1:
        for winner in winners:
            winner_names.append(state.players[winner].name)
        print('Winners are', winner_names, '\n')
    else:
        winner_names.append(state.players[winners[0]].name)
        print('Winner is', state.players[winners[0]].name, '\n')
    # return # state.players[np.argmax(payout)]
    return winner_names


def rotate(lst, n):
    n = n % len(lst)
    return lst[n:] + lst[:n]


def play_multiple_rotations(players, num_rotations=None):
    rotation_winners = {}
    for player in players:
        if player.name not in rotation_winners:
            rotation_winners[player.name] = 0
    if num_rotations is None:
        num_rotations = len(players)
    for rotation in range(num_rotations):
        print('-------- Rotation', rotation, '--------')
        current_rot = rotate(players, rotation)
        print('Current in-game positions', current_rot, '\n')

        #winners = play_game(current_rot)
        if all(x > 1 for x in [p.amount for p in current_rot]):
            winners = play_game(current_rot)
        else:
            break

        # print('WINNERS', winners)
        for winner in winners:
            rotation_winners[winner] += 1
        for player in players:
            player.bets = 1
            player.folded = False
            player.raised = False
    #print('Rotation Winners:', rotation_winners)
    return rotation_winners


def play_multiple_games(players, seed=42):

    random.seed(seed)
    keep_playing=True
    game_count=0
    looser={}
    while keep_playing:
        game_count=game_count+1
        print('-------- Game', game_count, '--------')
        random.shuffle(players)
        print('Initial game positions: ', players, '\n')
        #rotation_winners = play_multiple_rotations(players)
        if all(x > 1 for x in [p.amount for p in players]):
            rotation_winners = play_multiple_rotations(players)
        else:
            keep_playing=False
            print('Final game positions: ', players, '\n')
            for p in players:
                if p.amount<=1:
                    looser[p.name]=+1

            return(looser,players)



def play_tournament(num_matches=100, collusion=False):
    looser_total={}
    amount_total={}
    for i in range(num_matches):
        print('x' * 200)
        print("Match No:",i)
        #players = [RandomPlayer('Random'), RaisePlayer('Raise'), CallPlayer('Call')]
        #players = [ColludePlayer('leader'), RaisePlayer('victim'), ColludePlayer('follower')]

        if collusion==False:
            players = [RaisePlayer('leader'), RaisePlayer('victim'), RaisePlayer('follower')]
            players[0].collude_starter=0   #player 0 is the player who is being followed
            players[1].victim=0 # player being cheated/colluded out
            players[2].collude_follower=0  #player 2 copy player 0's action
        else:
            players = [ColludePlayer('leader'), RaisePlayer('victim'), ColludePlayer('follower')]
            players[0].collude_starter = 1  # player 0 is the player who is being followed
            players[1].victim = 1  # player being cheated/colluded out
            players[2].collude_follower = 1  # player 2 copy player 0's action
        looser,players=play_multiple_games(players)
        print("looser:",looser)
        for keys in looser:
            looser_total[keys]=looser_total[keys]+1 if keys in looser_total else 1
        for p in players:
            amount_total[p.name]=amount_total[p.name]+p.amount if p.name in amount_total else p.amount

        print("looser_total",looser_total, "amount_total:", amount_total, amount_total['leader']+amount_total['follower'])


def main():
    play_tournament()

if __name__ == "__main__":
    main()