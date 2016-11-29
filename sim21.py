# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

@author: rli
"""

import numpy as np
import random
import math
import pandas as pd

import pdb


# GLOBAL VARIABLES
GAME_DECK = []
DISCARD_DECK = []
possible_actions = ['H','St','Sp','D']


def init_game(num_decks, player_name, player_cash, num_players):
    """
    Function to initialize the game by creating a shuffled GAME_DECK and data frame for all players.
    Global variables GAME_DECK and DISCARD_DECK will be modified.
        Args: # of GAME_DECKs, name of current player, total # of players
        Returns: PLAYERS (pandas data frame)
    """
    # aggregate all GAME_DECKs into one shuffled GAME_DECK
    global GAME_DECK
    global DISCARD_DECK
    
    GAME_DECK = GAME_DECK + ['J']*(4*num_decks)
    GAME_DECK = GAME_DECK + ['Q']*(4*num_decks)
    GAME_DECK = GAME_DECK + ['K']*(4*num_decks)
    GAME_DECK = GAME_DECK + ['A']*(4*num_decks)
    for n in range(2,11):
        GAME_DECK = GAME_DECK + [n]*(4*num_decks)
    random.shuffle(GAME_DECK)
    
    DISCARD_DECK = [] # clear discard deck    
    
    index = ['Dealer', player_name]
    for p in range(0,num_players-1):
        index.append('Player ' + str(p+2))
    columns = ['Hand', 'Score', 'Cash']
    PLAYERS = pd.DataFrame(index=index, columns=columns)
    PLAYERS.loc["Dealer" , "Cash"] = 'Infinite'
    PLAYERS.loc[1:, "Cash"] = player_cash
    
    return PLAYERS
    

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


def deal_card(PLAYERS, p, show_card):
    """
    Deal a new card to player p and update score
    """
    global GAME_DECK

    card_drawn = GAME_DECK[0]
    
    hand = PLAYERS.loc[p, 'Hand']
    if type(hand) is float:
        if math.isnan(hand):
            # first card of a new game
            hand = []

    if show_card == 1:
        hand.append(GAME_DECK[0])
        PLAYERS.set_value(p, 'Hand', hand)
    
    GAME_DECK.pop(0)

    return PLAYERS, card_drawn
    

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
    

def sim_round(PLAYERS, player_name, player_bet):
        
    player_list = PLAYERS.index.tolist()
    
    # deal first card to each player
    for p in player_list:
        PLAYERS, hidden_card = deal_card(PLAYERS, p, 0)

    # deal second card to each player
    for p in player_list:
        if p is 'Dealer':
            # dealer's second card is hidden
            PLAYERS, dealer_last_card = deal_card(PLAYERS, p, 1)
        else:
            PLAYERS, = deal_card(PLAYERS, p, 0)
        
    pdb.set_trace()
    
    # update scores
    PLAYERS = calc_scores(PLAYERS)
    
    print('\n')
    print(PLAYERS.to_string()) 
    
    player_action = query_action() # query for action
    
    # decide/execute action for each player

    
    # decide/execute action for dealer
 
    pdb.set_trace()
    
    return PLAYERS

    
    
    
    print('\n')
    print(PLAYERS.to_string())
    
    return PLAYERS



def compute_prob():
    """
    Probability dictionary
    """
    global GAME_DECK
    global DISARD_DECK
    
    pdb.set_trace()
    return 0



if __name__ == "__main__":
    
    # SET SIMULATION PARAMETERS
    # player_name = input('Enter your name: ')
    player_name = 'Ronny'
    num_players = 3
    num_decks = 1
    player_cash = 2500

    # initialize game
    PLAYERS = init_game(num_decks, player_name, player_cash, num_players)
    
    # START GAME
    play = 1

    while play:
        
        # query player for bet
        # player_bet = query_bet(15)
        player_bet = 25
        if player_bet is 0:
            play = 0
            break
        
        PLAYERS = sim_round(PLAYERS, player_name, player_bet)
        
        # print round results
        
        # discard all cards in play
        
        # reset player hands

    # print game summary
    
            
        

    