# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

@author: rli
"""

import numpy as np
import math
import pandas as pd

import pdb

# Global variables
actions = ['H','St','Sp','D'] # hit, stand, split, double

class player():

    def __init__(self):
        self.hand = []

    def query_bet(self, player_cash, min_bet):
        '''
        Queries the user for a bet and checks that it is valid
        '''
        valid_bet = False
        while not valid_bet:
            bet = input('Place bet ($' + str(player_cash) + ' available): ')
            try:
                bet = int(bet)
                if (bet > player_cash):
                    print('Bet cannot exceed $' + str(player_cash))
                elif (bet < min_bet) and (bet is not 0):
                    print('Minimum bet is ' + str(min_bet))
                else:
                    valid_bet = True
            except ValueError:
                print('Bet must be an integer')
        return bet


    def query_action(self, game, deck, player):
        '''
        Queries user for one of the possible actions
        '''
        query_action = True
        while query_action:
            user_action = input('Type H to hit, St to stay, Sp to split, D to double down: ')
            if user_action == 'H':
                game = deal(game, player, deck.pop(0))
                print(game)
            elif user_action == 'St':
                query_action = False
            elif user_action == 'Sp':
                pdb.set_trace()
            elif user_action == 'D':
                pdb.set_trace()
            else:
                print('Invalid choice - try again')
        return game


    def deal(self, game, player, card_drawn):
        '''
        Deals one card to the specified player
            Returns: updated GAME dataframe
        '''
        # TODO: call cardCounter functions to update deck state whenever a card is drawn

        if game.loc[player,'Hand'] == 0:
            game.loc[player,'Hand'] = [str(card_drawn)]
        else:
            # TODO: encrypt dealer's
            game.loc[player,'Hand'].append(str(card_drawn))

        # pdb.set_trace()

        return game


    def calc_scores(self, game):
        '''
        Sum up the cards in each player's hand
            Returns: updated GAME dataframe
        '''
        for player in game.index:
            hand = game.loc[player, 'Hand']
            score = 0
            for card in hand:
                if (card is 'J'):
                    score = score + 10
                elif (card is 'Q'):
                    score = score + 10
                elif (card is 'K'):
                    score = score + 10
                elif (card is 'A'):
                    score = score + 10
                else:
                    score = score + int(card)
            game.set_value(player, 'Score', score)

        return game
