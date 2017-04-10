# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

@author: rli
"""

import numpy as np
import math
import random
import pandas as pd
import cardCounter as cc

import pdb


# Global variables
GAME_DECK = []
DISCARD_DECK = []
possible_actions = ['H','St','Sp','D']


def query_params ():
    '''
    Set simulation parameters
    '''    
    # define params dict
    sim_params = {'pName':[], 'pCash':[], 'numPlayers':[], 
    'numDecks':[], 'minBet':[]}

    # query user for inputs
#    sim_params['pName'] = input('What is your name? ')
#    sim_params['minBet'] = int(input('What is the minimum bet at this table? (10-100) '))
#    sim_params['numDecks'] = int(input('How many decks are used? (1-8) '))
#    sim_params['numPlayers'] = int(input('How many other players at the table? (0-4) '))
#    sim_params['pCash'] = int(input('How much cash are you throwing down? (100-2500) '))
    
    # dev mode
    sim_params['pName'] = 'Ronny'
    sim_params['minBet'] = 25
    sim_params['numDecks'] = 2
    sim_params['numPlayers'] = 2
    sim_params['pCash'] = 400

    return sim_params

    
def init_game(params):
    """
    Function to initialize the game by creating a shuffled dict GAME DECK and a 
    data frame PLAYERS containing playe information.
    Global variables GAME_DECK and DISCARD_DECK will be modified.
        Args: # of GAME_DECKs, name of current player, total # of players
        Returns: PLAYERS (pandas data frame)
    """
    global GAME_DECK
    global DISCARD_DECK
    
    for card in ['J','Q','K','A']:
        GAME_DECK = GAME_DECK + [card]*(4*params['numDecks'])

    for n in range(2,11):
        GAME_DECK = GAME_DECK + [n]*(4*params['numDecks'])
        
    random.shuffle(GAME_DECK)

    index = [params['pName']]
    for p in range(0,params['numPlayers']):
        index.append('Player ' + str(p+2))
    index.append('Dealer')
        
    columns = ['Hand', 'Score', 'Cash']
    PLAYERS = pd.DataFrame(index=index, columns=columns)
    PLAYERS = PLAYERS.fillna(0) # fill with 0's instead of nan's
    PLAYERS.loc["Dealer" , "Cash"] = 'Inf'
    PLAYERS.loc[0:-1, "Cash"] = params['pCash']
    
    return PLAYERS


def deal(PLAYERS, p, show_flag):
    """
    Deal a new card to player p
        Args: 
        Returns: Updated GAME_DECK dict and PLAYERS data frame
    """
    global GAME_DECK
    global DISCARD_DECK
    
    # pop the top card off the game deck
    card_drawn = GAME_DECK.pop(0)
    DISCARD_DECK.append(card_drawn)

    if PLAYERS.loc[p, "Hand"] == 0:
        PLAYERS.loc[p, "Hand"] = [str(card_drawn)]
    else:
        if show_flag:
            PLAYERS.loc[p, "Hand"].append(str(card_drawn))
        else:
            PLAYERS.loc[p, "Hand"].append('?')

    return PLAYERS, card_drawn


def query_bet(params, pCash):
    '''
    Queries the user for a bet and checks that it is valid
    '''
    bet = int(input('Place bet ($' + str(params['minBet']) + ' - ' + str(pCash) + '): '))

    return bet
    
    
def query_action():
    '''
    Queries the user for one of the possible actions and checks that it is valid
    '''
    global possible_actions
    
    valid_action = 0
    while valid_action == 0:
        action = input('What would you like to do? (H = Hit, St = Stay, \
        Sp = Split, DD = Double down) ')
        if action in possible_actions:
            valid_action = 1
    
    return action
  
    


if __name__ == "__main__":
    
    sim_params = query_params()
    
    PLAYERS = init_game(sim_params)

    # Loop game until stopped by user
    play = 1
    
    while play:
        
        user_bet = query_bet(sim_params, PLAYERS.loc[sim_params['pName'], "Cash"])

        # first card face-up to each player
        for n in range(0,len(PLAYERS)-1):
            PLAYERS, card_drawn = deal(PLAYERS, PLAYERS.index[n], 1)
        
        # second card face-up to each player
        for n in range(0,len(PLAYERS)-1):
            PLAYERS, card_drawn = deal(PLAYERS, PLAYERS.index[n], 1)
            
        # one face-up card to dealer
        PLAYERS, card_drawn = deal(PLAYERS, 'Dealer', 1)

        # face-down card to dealer
        PLAYERS, dealer_card = deal(PLAYERS, 'Dealer', 0)
        
        # display current state
        print(PLAYERS)
        
        pdb.set_trace()
        
        # query actions
        user_action = query_action()
            
    
    