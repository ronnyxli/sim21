# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

@author: rli
"""

import numpy
import itertools
import argparse
import random

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
    # returns a full shuffled deck
    DECK = []
    DECK.append(['J']*(4*N))
    DECK.append(['Q']*(4*N))
    DECK.append(['K']*(4*N))
    for n in range(1,11):
        DECK.append([n]*(4*N))
    DECK = list(itertools.chain.from_iterable(DECK))
    random.shuffle(DECK)
    return DECK



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
    arg_dict = parse_args()   
    
    playerName = input('Enter your name: ')
    
    # initialize deck 
    DECK = new_deck(arg_dict['NUM_DECKS'])
    playerCash = arg_dict['NUM_CREDITS']

    # number of each card type  
    N = arg_dict['NUM_DECKS']
    CARDS = {'H':12*N, '1':4*N, '2':4*N, '3':4*N, '4':4*N, '5':4*N, '6':4*N, 
            '7':4*N, '8':4*N, '9':4*N, '10':4*N}
    
    # start game
    playFlag = 1
    state = {'Dealer':[], playerName:[]}
    
    while playFlag:
        
        # query player for bet
        validBet = 0
        while (validBet == 0):
            bet = int(input('Place bet ($' + str(playerCash) + ' available): '))
            if (bet > playerCash):
                print('Bet cannot exceed $' + str(playerCash))
            elif (bet < 1):
                print('Bet must be at last $1')
            else:
                validBet = 1
        
        # deal cards
        
                
        
        action = input('Type H for hit, S for stand: ')
    
    
    
    
    
    
    arg_dict['NUM_PLAYERS']
    arg_dict['NUM_CREDITS']
    
    
    


