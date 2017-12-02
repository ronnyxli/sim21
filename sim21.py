# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

Functions to simulate Blackjack

@author: rli
"""

import numpy as np
import math
import pandas as pd

import pdb


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
    params['num_players'] = 1
    params['player_cash'] = 400

    return params


def display(player_list):
    '''
    Prints all player cash and hands
    '''
    print('\n')
    for p in player_list:
        print(p.name + ' ($' + str(p.cash) + '): ' + p.showHand())
    print('\n')


def query_bet(player_cash, min_bet):
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


def query_action():
    '''
    Queries user for one of the possible actions
    '''
    query_action = True
    while query_action:
        user_action = input('Type H to hit, St to stay, Sp to split, D to double down: ')
        if user_action not in ['H','St','Sp','D','exit']:
            print('Invalid choice - try again')
        else:
            query_action = False
    return user_action
