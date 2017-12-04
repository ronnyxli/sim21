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
    # params['playerName'] = input('What is your name? ')
    # params['minBet'] = int(input('What is the minimum bet at this table? (10-100) '))
    # params['numDecks'] = int(input('How many self.decks are used? (1-8) '))
    # params['numPlayers'] = int(input('How many other players at the table? (0-4) ')) + 1
    # params['playerCash'] = int(input('How much cash are you throwing down? (100-2500) '))

    # dev mode
    params = {'playerName':'Ronny', 'minBet':25,
                'numDecks':2, 'numPlayers':1, 'playerCash':400}

    return params


def display_cards(player_list, flag):
    '''
    Prints all player cash and hands
        Args: List of Player class instance
    '''
    print('\n')
    for p in player_list:
        print(p.name + ' ($' + str(p.cash) + '): ' + str(p.showHand(flag)))
    print('\n')


def query_bet(player_cash, min_bet):
    '''
    Queries the user for a bet and checks that it is valid
    '''
    valid_bet = False
    while not valid_bet:
        bet = input('Specify bet ($' + str(player_cash) + ' available) or type "leave": ')
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
        if user_action in ['leave', 'exit', 'stop', 'quit']:
            print("You can't fucking leave in the middle of a round, asshole.")
        elif user_action not in ['H','St','Sp','D']:
            print('Invalid choice - try again')
        else:
            query_action = False
    return user_action


# def calc_results(player_list):
