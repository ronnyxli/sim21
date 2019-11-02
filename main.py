'''
Ronny Li

Initial version: September 13, 2019

Usage:
    main.py (--play|--sim)

Options:
    -h, --help              Show this screen
    --play|--sim            Gameplay (interactive) or simulation mode
'''

import pandas as pd
import random
from docopt import docopt
from collections import defaultdict
import sim
import pdb


def init_game():
    '''
    Get parameters of game and initialize list of player dicts
    '''

    params = defaultdict(int)
    params['num_decks'] = 4
    params['num_players'] = 5
    params['player_position'] = 5
    params['min_bet'] = 5
    params['max_bet'] = 50
    params['starting_cash'] = 200
    params['bj_payout'] = 6/5
    player_name = 'Ronny'

    player_list = []
    for n in range(0,params['num_players']):
        if n == params['player_position']-1:
            # user
            player_dict = {'Name':player_name,
                           'Hands':[],
                           'Cash': params['starting_cash']}
        else:
            # simulated player
            player_dict = {'Name':'P' + str(n),
                           'Hands':[],
                           'Cash': params['starting_cash']}
        player_list.append(player_dict)

    return params, player_list


class Deck(object):

    def __init__(self, num_decks):
        # initialize deck as list of cards
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*num_decks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*num_decks)
        random.shuffle(self.cards)
        # initialize dict for state variables
        self.state = {'numHi':16*num_decks, 'numAce':4*num_decks}
        # TODO: probability matrix?

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop(0)
        if card in ['J','Q','K',10]:
            self.state['numHi'] = self.state['numHi'] - 1
        elif card == 'A':
            self.state['numAce'] = self.state['numAce'] - 1
        return card

    def update(self):
        '''
        Update state variables and probability matrix
        '''
        pdb.set_trace()


class Hand(object):

    def __init__(self):
        self.cards = []
        self.score = 0
        self.win_prob = 0

    def calc_score(self):
        for card in self.cards:
            if card in ['J','Q','K']:
                # face card - add 10
                self.score += 10
            elif card in range(2,11):
                # add card value
                self.score += card
            else:
                # ace - add 1 or 11
                self.score += 11
                if self.score > 21:
                    self.score -= 10


def main(args):

    params, players = init_game()
    MasterDeck = Deck(params['num_decks'])
    dealer_hand = Hand()

    PLAY = True
    while PLAY:

        # query player bet
        if args['--play']:
            player_bet = sim.query_bet(params['min_bet'], params['max_bet'])
        else:
            player_bet = sim.sim_bet(params['min_bet'], params['max_bet'])

        if not player_bet:
            # leave game
            break

        # TODO: set player bet

        # TODO: simulate bets for other players; query bet for user if gamelay mode
        

        # initial deal - 2 cards to each player and dealer
        pdb.set_trace()
        sim.deal(MasterDeck, dealer_hand, players, 2)

        pdb.set_trace()


        # TODO: loop through all players - simulate bets and query bet for user if gameplay mode

    # TODO: print summary
    pdb.set_trace()

    # TODO: initialize player dict

if __name__ == '__main__':
    main(docopt(__doc__))
