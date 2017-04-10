# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 12:08:15 2017

@author: rli
"""

import pandas as pd
import random
import math

import pdb


# Global variables








def query_bet(min_bet):
    """
    Queries user for the amount of $ to bet
    """
    valid_bet = 0
    while (valid_bet == 0):
        bet = input('Place bet ($' + str(player_cash) + ' available): ')
        try:
            bet = int(bet)
            if (bet > player_cash):
                print('Bet cannot exceed $' + str(player_cash))
            elif (bet < min_bet) and (bet is not 0):
                print('Minimum bet is ' + str(min_bet))
            else:
                valid_bet = 1
        except ValueError:
            print('Bet must be an integer')
    return bet


def query_action():
    """
    Queries user for an action based on the current hand
    """
    query_action = 1
    while query_action:
        action = input('Type H to hit, St to stay, Sp to split, D to double down: ')
        if action in possible_actions:
            query_action = 0
        else:
            print('Invalid choice - try again')
    return action 





def calc_scores(PLAYERS):
    """
    Sum up the cards in each player's hand and update PLAYERS data frame with the score
    """    
    ind = PLAYERS.index.tolist()   
    
    for p in range(0,len(ind)):
        hand = PLAYERS.loc[ind[p] , 'Hand']
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
        PLAYERS.set_value(ind[p], 'Score', score) 
   
    return PLAYERS