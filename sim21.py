# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

Functions to simulate Blackjack game

@author: rli
"""

import numpy as np
import math
import pandas as pd

import pdb


def init_game(dev_mode):
    '''
    Set simulation parameters
        Returns: Shuffled self.deck as list, game GAME as dataframe
    '''

    if dev_mode:
        params = {'playerName':'Ronny', 'minBet':25, 'numDecks':2,\
            'numOpponents':4, 'playerPos':1, 'playerCash':500,\
            'mode':1, 'scheme':'HiLo'}
    else:
        params = {}
        # query user for inputs
        params['playerName'] = input('What is your name? ')
        params['minBet'] = int(input('What is the minimum bet at this table? (10-100) '))
        params['numDecks'] = int(input('How many decks are used? (1-8) '))
        params['numOpponents'] = int(input('How many other players are at the table? (0-4) '))
        params['playerPos'] = int(input('Which seat are you in? (1-' + str(params['numOpponents']+1) + ') ')) - 1
        params['playerCash'] = int(input('How much cash are you throwing down? (100-2500) '))
        params['mode'] = int(input('1 for game play, 2 for simuation: '))
        params['scheme'] = input('Card-counting scheme: ')

    # create list of players
    player_list = []
    for n in range(0,params['numOpponents']+2):
        player_dict = {'Name':'Player' + str(n),\
            'Cards':[[]], 'Cash':params['playerCash'], 'Bet':[]}
        player_list.append(player_dict)

    # replace first spot with user and last spot with dealer
    player_list[params['playerPos']]['Name'] = params['playerName']
    player_list[-1]['Name'] = 'Dealer'

    return params, player_list


def score(x):
    '''
    Calculate a score given hand x
        Args: List of cards
        Returns: Optimized score of cards
    '''
    points = 0
    num_aces = 0
    if len(x) > 0:
        for card in x:
            if card in ['J','Q','K']:
                points = points + 10
            elif card == 'A':
                num_aces = num_aces + 1
            else:
                points = points + int(card)
    for n in range(0,num_aces):
        if (points + 11) > 21:
            points = points + 1
        else:
            points = points + 11
    return points


def show_cards(player_list, first):
    '''
    Prints all player cash and hands
        Args: List of Player class instance
    '''
    if first:
        # find dealer and hide the first card of his/her first hand
        dealer_idx = [x['Name'] for x in player_list].index('Dealer')
        player_list[dealer_idx]['Cards'][0][0] = '?'
    print(pd.DataFrame(player_list))


def split(x, new_cards):
    '''
    Split hand x into two hands
    '''
    y = []
    pdb.set_trace()
    return y
    

def query_bet(player_list, bet_range):
    '''
    Queries the user for a bet and checks that it is valid
    '''
    valid_bet = False
    while not valid_bet:
        bet = input('Specify bet between $' + str(bet_range[0]) + \
            ' and $' + str(bet_range[1]) + ' or type 0 to leave: ')
        try:
            bet = int(bet)
            if (bet > bet_range[1]):
                print('Bet cannot exceed $' + str(bet_range[1]))
            elif (bet < bet_range[0]) and (bet is not 0):
                print('Minimum bet is ' + str(bet_range[0]))
            else:
                valid_bet = True
        except ValueError:
            print('Bet must be an integer')

    # clear hand(s) and assign bet for all players
    for n in range(0,len(player_list)):
        # note that each player's cards is represented by a list of lists
        player_list[n]['Cards'] = [[]]
        player_list[n]['Bet'] = bet

    return player_list


def auto_bet(player_cash, min_bet, deck_state):
    '''
    Simulate the bet based on the state of the remaining cards
    '''
    pdb.set_trace()

    return bet


def query_decision(options):
    '''
    Queries user for one of the possible actions
    '''
    query_action = True
    while query_action:
        user_action = input('Type H to hit, St to stay, Sp to split, D to double down: ')
        if user_action in ['leave', 'exit', 'stop', 'quit']:
            print("You can't fucking leave in the middle of a round, asshole.")
        elif user_action not in options:
            print('Invalid choice - try again')
        else:
            query_action = False
    return user_action


def auto_decision(inp):
    '''
    Simulates by-the-book decision for cards in hands inp
    '''
    for x in inp:
        if score(x) < 17:
            action = 'H'
        else:
            action = 'St'
        return action

























def calc_results(cards, bet, dealer_score):
    '''
    Compares current hand (defined by cards) to dealer_score
        and deduct win/loss specified by bet
    '''
    winnings = 0
    if score(cards) > 21:
        # player busts
        if dealer_score <= 21:
            # dealer doesn't bust
            winnings = winnings - bet
    else:
        # player does not bust
        if dealer_score > 21:
            # dealer busts
            winnings = winnings + bet
        else:
            # both player and dealer don't bust
            if (score(cards) > dealer_score):
                # player has higher score
                winnings = winnings + bet
            elif (score(cards) < dealer_score):
                # dealer has higher score
                winnings = winnings - bet
    return winnings
