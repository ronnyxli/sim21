#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:40:05 2017

@author: ronnyli
"""

import numpy as np
import pandas as pd

import sim21 as sim
from deckManager import Deck

import pdb


# global variables



def init_game():
    '''
    Set simulation parameters
        Returns: Shuffled self.deck as list, game GAME as dataframe
    '''
    params = {}

    # query user for inputs
    # params['player_name'] = input('What is your name? ')
    # params['min_bet'] = int(input('What is the minimum bet at this table? (10-100) '))
    # params['num_decks'] = int(input('How many self.decks are used? (1-8) '))
    # params['num_players'] = int(input('How many other players at the table? (0-4) ')) + 1
    # params['player_cash'] = int(input('How much cash are you throwing down? (100-2500) '))

    # dev mode
    params['player_name'] = 'Ronny'
    params['min_bet'] = 25
    params['num_decks'] = 2
    params['num_players'] = 3
    params['player_cash'] = 400

    return params



class Player(object):
    '''
    '''

    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.hand = [] # list of cards in player's hand

    def reset(self):
        self.hand = []

    def score(self):
        '''
        Calculate score of player's hand
        '''
        points = 0
        if len(self.hand) > 0:
            for card in self.hand:
                if card in ['J','Q','K']:
                    points = points + 10
                elif card == 'A':
                    points = points + 1
                else:
                    points = points + int(card)
        # TODO: optimize value of A[s]
        return points



if __name__ == "__main__":

    params = init_game()

    GameDeck = Deck(params['num_decks'])

    Dealer = Player('Dealer', 0)

    # list of Player class instances
    Players = []
    for n in range(0,params['num_players']):
        if n == 0:
            Players.append(Player(params['player_name'], params['player_cash']))
        else:
            Players.append(Player('Player' + str(n), params['player_cash']))

    # start game
    play = True
    while play:

        # deal one card to each player
        for n in range(0,len(Players)):
            Players[n].reset()
            Players[n].hand.append(GameDeck.deal())
        # last card to dealer
        Dealer.hand.append(GameDeck.deal())

        

    # TODO: last step: print game summary
