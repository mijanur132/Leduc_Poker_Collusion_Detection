import numpy as np

from copy import copy, deepcopy
from leduc.players.player import Player


class State:
    def __init__(self, cards, num_players, hand_eval):
        self.num_players = num_players
        self.num_active_players = num_players
        self.num_rounds = 1
        self.eval = hand_eval
        self.cards = cards
        self.players = [Player(str(_)) for _ in range(num_players)]
        self.history = [[] for _ in range(self.num_rounds)]
        self.round = 0
        self.turn = 0
        self.terminal = False
                                #for collusion play
        self.colludLeader=0
        self.colludFollower=0
        self.victim=0

    def __repr__(self):
        return f"{self.history[:self.round + 1]}"

    def __eq__(self, other):
        return self.history == other.history and self.cards == other.cards

    def __hash__(self):
        return hash(f'{self.history}, {self.cards}')

    def __copy__(self):
        new_state = State(self.cards, self.num_players, self.eval)
        new_state.players = deepcopy(self.players)
        new_state.history = deepcopy(self.history)
        new_state.turn = self.turn
        new_state.terminal = self.terminal
        new_state.round = self.round

        return new_state

    def info_set(self):
        hole_card = self.cards[self.turn]
        if len(self.cards) > len(self.players):
            board_card = self.cards[len(self.players)]
        else:
            board_card = None

        info_set = f"{hole_card} |{board_card if board_card is not None else ''}| {str(self)}"
        return info_set

    def take(self, action, deep=False):
        if self.terminal:
            raise ValueError("Already at a terminal state")

        if deep is True:
            new_state = copy(self)
        else:
            new_state = self
        new_state.history[self.round].append(action)
        print("new_state.history:",new_state.history)
        curr_player = new_state.players[new_state.turn]
        if action == 'F':
            curr_player.folded = True
            curr_player.raised = False
            self.num_active_players -= 1

        elif 'R' in action:
            bet_amount = int(action[:-1])   #get int from 2R, 4R etc
            call_size = max(self.players).bets - curr_player.bets #level with current max
            curr_player.bets += bet_amount + call_size #add on top of max
            curr_player.raised = True

        else:
            call_size = max(self.players).bets - curr_player.bets
            curr_player.bets += call_size

        new_state.terminal = new_state.is_terminal()

        return new_state

    def is_terminal(self):
        num_folded = sum([p.folded for p in self.players])
       # print("num folded:",num_folded)
        if num_folded == self.num_players - 1:
          #  print("Terminal because,", num_folded, " equals num_players-1. Mean everyone folded")
            return True

        num_actions = len(self.history[self.round])
        fold_actions = self.history[self.round].count('F')

        min_actions = self.num_players - (num_folded - fold_actions)#For a round when a folding happens, the folding will count towerd total action
        #print('Num actions:', num_actions, ' FOLD ACTIONS:', fold_actions," min actions:", min_actions)
        max_bet = max([p for p in self.players if p.folded is False],
                      key=lambda k: k.bets)  #which player has the max bet
        #print("max_bet_player:", max_bet)
        end_round = True
        for player in self.players:
            if not player.folded:
               # print("player<max_bet",player<max_bet, " player:",player)
                if player < max_bet:
                  #  print("Not end round, there are players, max bet is not covered")
                    end_round = False

        if num_actions >= min_actions and end_round:  #at least all active players should take actions even if end round
           # print("End round")
            if self.round == self.num_rounds - 1:
               # print("Terminate cause, self.round:", self.round, " is equal to (self.num_rounds-1)=", self.num_rounds-1, )
                return True
            else:
                self.round += 1
                self.turn = 0
                for p in self.players:
                    p.raised = False

                return False

        self.turn = (self.turn + 1) % self.num_players #go for the next player

        while self.players[self.turn].folded:   #skip the folded player(s)
            self.turn = (self.turn + 1) % self.num_players

        return False

    def utility(self):
        if len(self.players) - sum([p.folded for p in self.players]) == 1:
            hand_scores = []
            winners = [i for i, _ in enumerate(self.players) if self.players[i].folded == False]

        else:
            board_cards = None if len(self.cards) <= self.num_players else [self.cards[self.num_players]]
            players_in = [i for i, p in enumerate(self.players) if p.folded == False]
            hand_scores = [self.eval(self.cards[i], board_cards) for i in players_in]
            print("playersIn:",players_in)
            print("hand scores:",hand_scores)
            winners = []
            high_score = -1
            for i, score in zip(players_in, hand_scores):
                if not self.players[i].folded:
                    if len(winners) == 0 or score > high_score:
                        winners = [i]
                        high_score = score
                    elif score == high_score:
                        winners.append(i)

        pot = sum(self.players)
        print('winners', winners)
        payoff = pot / len(winners)
        payoffs = [-p.bets for p in self.players]
        print("payoffs:",payoffs)
        for w in winners:
            payoffs[w] += payoff
        # Keep track of amount with player
        for idx, p in enumerate(self.players):
            p.amount += payoffs[idx]
        print("updaetd payoffs",payoffs)
        return np.array(payoffs)

    def valid_actions(self):
        any_raises = any([p.raised for p in self.players])
        if any_raises:
            return ['F', 'C']

        return ['F', 'C', '1R']


class Leduc(State):
    def __init__(self, cards, num_players, hand_eval, players=None):
        super().__init__(cards, num_players, hand_eval)
        self.num_rounds = 2
        if not players:
            self.players = [Player() for _ in range(num_players)]
        else:
            self.players = players
        self.history = [[] for _ in range(self.num_rounds)]

    def __copy__(self):
        new_state = Leduc(self.cards, self.num_players, self.eval)
        new_state.players = deepcopy(self.players)
        new_state.history = deepcopy(self.history)
        new_state.turn = self.turn
        new_state.terminal = self.terminal
        new_state.round = self.round

        return new_state

    def valid_actions(self,curr_player):
        num_raises_so_far = sum([p.raised for p in self.players])

        if num_raises_so_far == self.num_active_players:
            return ['F', 'C']
        else:
            if self.round == 0:
                return ['F', 'C', '2R']
            else:
                return ['F', 'C', '4R']

    # def valid_actions(self, curr_player, num_raises_allowed=2):
    #     # @TODO: What if the player has no money - then need to wait till end of round to see if they won anything.
    #     # Right now the player is just folding if they don't have enough money.
    #     num_raises_so_far = sum([p.raised for p in self.players])
    #     call_size = max(self.players).bets - curr_player.bets
    #
    #     if num_raises_so_far == num_raises_allowed:
    #         if curr_player.amount - curr_player.bets >= call_size:
    #             return ['F', 'C']
    #         else:
    #             return ['F']
    #     else:
    #         if self.round == 0:
    #             if curr_player.amount - curr_player.bets - call_size >= 2:
    #                 return ['F', 'C', '2R']
    #             elif curr_player.amount - curr_player.bets >= call_size:
    #                 return ['F', 'C']
    #             else:
    #                 return ['F']
    #         else:
    #             if curr_player.amount - curr_player.bets - call_size >= 4:
    #                 return ['F', 'C', '4R']
    #             elif curr_player.amount - curr_player.bets >= call_size:
    #                 return ['F', 'C']
    #             else:
    #                 return ['F']

    def get_current_state(self):
        current_state = {'players':self.players,
                         'history': self.history, 'hole_card': self.cards[self.turn],
                         'board_card': None if len(self.cards) <= self.num_players or self.round == 0 else
                         self.cards[self.num_players],
                         'round': 'pre_flop' if self.round == 0 else 'flop'}
        return current_state
