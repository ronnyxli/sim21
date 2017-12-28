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


def init_game():
    '''
    Set simulation parameters
        Returns: Shuffled self.deck as list, game GAME as dataframe
    '''
    params = {}

    # game mode: query user for inputs
    '''
    params['playerName'] = input('What is your name? ')
    params['minBet'] = int(input('What is the minimum bet at this table? (10-100) '))
    params['numDecks'] = int(input('How many decks are used? (1-8) '))
    params['numPlayers'] = int(input('How many other players at the table? (0-4) ')) + 1
    params['playerCash'] = int(input('How much cash are you throwing down? (100-2500) ')
    '''

    # dev mode
    params = {'playerName':'Ronny', 'minBet':25,
                'numDecks':2, 'numPlayers':1, 'playerCash':400}

    return params


def score(x):
    '''
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


def display_cards(player_list, flag):
    '''
    Prints all player cash and hands
        Args: List of Player class instance
    '''
    print('\n')
    for p in player_list:
        hands_str = p.name + ' ($' + str(p.cash) + '): ' + '| '
        # loop all hands
        for hand in p.hands:
            if (p.name == 'DEALER') & (not flag):
                # second card dealt face-down
                hands_str = hands_str + str(hand['cards'][0]) + ' ? '
            else:
                for card in hand['cards']:
                    hands_str = hands_str + str(card) + ' '
                hands_str = hands_str + '(' + str(score(hand['cards'])) + ') '
            hands_str = hands_str + '| '
        print(hands_str)
    print('\n')


def query_bet(player_cash, min_bet):
    '''
    Queries the user for a bet and checks that it is valid
    '''
    valid_bet = False
    while not valid_bet:
        bet = input('Specify bet ($' + str(player_cash) + \
                ' available, ' + '$' + str(min_bet) + ' minimum) ' + \
                'or type 0 to leave: ')
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


def simAction(cards):
    '''
    Simulates by-the-book decision for cards in the hand
    '''
    if score(cards) < 17:
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
