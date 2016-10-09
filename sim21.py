# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

@author: rli
"""

import numpy
import itertools
import argparse
import random
import pandas as pd

import pdb


# ARGUMENTS: 
# NUM_DECKS

def parse_args():
    # add arguments to parser
    parser = argparse.ArgumentParser(description = 'Simulation parameters')    
    parser.add_argument('-d', metavar='NumDecks', type=int, dest='num_decks',
        default=1, help='Number of card decks to use (default = 1, max = 8)') 
    parser.add_argument('-p', metavar='NumPlayers', type=int, dest='num_players',
        default=1, help='Number of players at the table (default = 1, max = 5)') 
    parser.add_argument('-c', metavar='NumCredits', type=int, dest='num_credits',
        default=500, help='Number of card decks to use (default = 500, max = 2500)') 
    # create dictionary of arguments 
    arg_dict = {}
    # check number of decks
    if (parser.parse_args().num_decks <= 8) & (parser.parse_args().num_decks >= 1):
        arg_dict['NUM_DECKS'] = parser.parse_args().num_decks
    else:
        print('Number of decks must be between 1 and 8... using default value of 1')
        arg_dict['NUM_DECKS'] = 1
    # check number of players
    if (parser.parse_args().num_players <= 5) & (parser.parse_args().num_players >= 1):
        arg_dict['NUM_PLAYERS'] = parser.parse_args().num_players
    else:
        print('Number of players must be between 1 and 5... using default value of 1')
        arg_dict['NUM_PLAYERS'] = 1
    # check number of credits
    if (parser.parse_args().num_credits <= 2500) & (parser.parse_args().num_credits >= 100):
        arg_dict['NUM_CREDITS'] = parser.parse_args().num_credits
    else:
        print('Cash must be between 100 and 2500... using default value of 500')
        arg_dict['NUM_CREDITS'] = 500
    return arg_dict
        

def new_deck(N):
    """
    Function to aggregate N decks into one shuffled deck
    """
    DECK = []
    DECK.append(['J']*(4*N))
    DECK.append(['Q']*(4*N))
    DECK.append(['K']*(4*N))
    for n in range(1,11):
        DECK.append([n]*(4*N))
    DECK = list(itertools.chain.from_iterable(DECK))
    random.shuffle(DECK)
    return DECK


def query_bet():
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
            elif (bet < 1):
                print('Bet must be at last $1')
            else:
                valid_bet = 1
        except ValueError:
            print('Bet must be an integer')
    return bet


def compute_prob(CARDS):
    # probability dictionary
    return 0


def deal(deck, cards, numPlayers):
    state = []
    
    # deal one card to each player first
    for p in range(0,numPlayers):
        deck[p]
    
    # one card to dealer
    
    # second card to each player
    
    # second card to dealer
    
    
    return deck, cards, state





if __name__ == "__main__":
    
    # parse arguments
    # arg_dict = parse_args()   
    
    # prompt user for info
    # player_name = input('Enter your name: ')
    player_names = 'Ronny'
    num_players = 5
    num_decks = 8
    player_cash = 2500
    
    # initialize deck
    DECK = new_deck(num_decks)
    
    # initialize pandas data frame for players
    
    PLAYERS = pd.DataFrame()

    # start game
    play = 1

    while play:
        
        # query player for bet
        bet = query_bet()
  
        # deal cards
        
        pdb.set_trace()         
        
        action = input('Type H to hit, S to stand, Q to quit: ')
    
        if action == 'H':
            break
        elif action == 'S':
            break
        elif action == 'Q':
            play = 0
        else:
            break
    
    
    
    
    arg_dict['NUM_PLAYERS']
    arg_dict['NUM_CREDITS']
    
    
    


