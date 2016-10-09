# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

@author: rli
"""

import numpy
import itertools
import random
import pandas as pd

import pdb


def init_game(num_decks, player_name, player_cash, num_players):
    """
    Function to initialize the game by creating a shuffled deck and data frame for all players
        Args: # of decks, name of current player, total # of players
        Returns: DECK (list of cards in random order), PLAYERS (pandas data frame)
    """
    # aggregate all decks into one shuffled deck
    DECK = []
    DECK.append(['J']*(4*num_decks))
    DECK.append(['Q']*(4*num_decks))
    DECK.append(['K']*(4*num_decks))
    DECK.append(['A']*(4*num_decks))
    for n in range(2,11):
        DECK.append([n]*(4*num_decks))
    DECK = list(itertools.chain.from_iterable(DECK))
    random.shuffle(DECK)
    
    index = ['Dealer', player_name]
    for p in range(0,num_players-1):
        index.append('Player ' + str(p+2))
    columns = ['Card 1', 'Card 2', 'Score', 'Cash']
    PLAYERS = pd.DataFrame(index=index, columns=columns)
    PLAYERS.loc["Dealer" , "Cash"] = 'Infinite'
    PLAYERS.loc[1:, "Cash"] = player_cash
    
    return DECK, PLAYERS
    

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
            elif (bet < min_bet):
                print('Minimum bet is ' + str(min_bet))
            else:
                valid_bet = 1
        except ValueError:
            print('Bet must be an integer')
    return bet


def calc_score(row):
    cards_ind = ['Card 1', 'Card 2']
    score = 0
    for c in cards_ind:
        if (row[c] is 'J'):
            score = score + 10
        elif (row[c] is 'Q'):
            score = score + 10
        elif (row[c] is 'K'):
            score = score + 10
        elif (row[c] is 'A'):
            score = score + 10
        else:
            score = score + row[c]      
    return score


def deal(DECK, PLAYERS):
    
    ind = PLAYERS.index.tolist()

    # deal first card to each player (dealer last?)
    for p in range(0,len(ind)):
        PLAYERS.set_value(ind[p], 'Card 1', DECK[p])
        
    # deal second card to each player (dealer hidden)
    for p in range(0,len(ind)):
        if ind[p] is "Dealer":
            dealer_last_card = DECK[p]
        else:
            PLAYERS.set_value(ind[p], 'Card 2', DECK[p])    
            # compute score
            score = calc_score(PLAYERS.loc[ind[p],:])
            PLAYERS.set_value(ind[p], 'Score', score)  
    
    return PLAYERS, dealer_last_card




def compute_prob(DECK):
    # probability dictionary
    return 0




if __name__ == "__main__":
    
    # prompt user for info
    # player_name = input('Enter your name: ')
    player_name = 'Ronny'
    num_players = 3
    num_decks = 1
    player_cash = 2500
    
    # initialize game
    DECK, PLAYERS = init_game(num_decks, player_name, player_cash, num_players)
    
    # START GAME
    play = 1

    while play:
        
        # query player for bet
        bet = query_bet(15)
        
        PLAYERS, dealer_last_card = deal(DECK, PLAYERS)
        
        print(PLAYERS.to_string())     
        
        query_action = 1
        while query_action:
        
            action = input('Type H to hit, St to stand, Sp to split, D to double, Q to quit: ')
    
            if action == 'H':
                query_action = 0
                pdb.set_trace()
                # add extra column
            elif action == 'St':
                query_action = 0
                pdb.set_trace()
            elif action == 'Sp':
                query_action = 0
                pdb.set_trace()
            elif action == 'D':
                query_action = 0
                pdb.set_trace()
            elif action == 'Q':
                query_action = 0
                play = 0
            else:
                print('Invalid choice')
    
    