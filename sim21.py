# -*- coding: utf-8 -*-
"""
Created on Sun Jul 31 19:57:40 2016

Functions to simulate Blackjack game

@author: rli
"""

import numpy as np
import pdb


def init_game():
    '''
    Set simulation parameters
        Returns: Shuffled self.deck as list, game GAME as dataframe
    '''
    params = {}

    # game mode: query user for inputs
    '''
    params['mode'] = input('Type sim for simulation mode, play for gameplay mode: ')
    params['maxHands'] = int(input('How many hands to simulate? '))
    params['playerName'] = input('What is your name? ')
    params['minBet'] = int(input('What is the minimum bet at this table? (10-100) '))
    params['numDecks'] = int(input('How many decks are used? (1-8) '))
    params['numPlayers'] = int(input('How many other players at the table? (0-4) ')) + 1
    params['playerCash'] = int(input('How much cash are you throwing down? (100-2500) ')
    '''

    # dev mode
    params = {'mode':'sim','maxHands':1000, 'playerName':'Ronny', 'minBet':25,
                'numDecks':2, 'numPlayers':1, 'playerCash':1000}

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


def query_action(actions):
    '''
    Queries user for one of the possible actions
    '''
    query = True
    while query:
        user_action = input('Choose one of the following ' + str(actions) + ': ')
        if user_action in ['leave', 'exit', 'stop', 'quit']:
            print("You can't fucking leave in the middle of a round, asshole.")
        elif user_action not in actions:
            print('Invalid choice - try again')
        else:
            query = False
    return user_action


def sim_player_action(cards, dealer_card):
    '''
    Simulates by-the-book decision for a player
    '''
    # pdb.set_trace()
    pScore = score(cards) # player score
    dScore = score([dealer_card]) # dealer score
    if cards.count('A') == 2:
        action = 'Sp'
    else:
        if 'A' in cards:
            # soft hands
            if dScore < 7:
                # dealer holding 2-6
                if pScore < 16:
                    action = 'H'
                elif pScore < 19:
                    action = 'D'
                else:
                    action = 'St'
            else:
                # dealer holding 7-A
                if pScore < 17:
                    action = 'H'
                else:
                    action = 'St'
        else:
            # hard hands
            if dScore < 7:
                # dealer holding 2-6
                if pScore < 9:
                    action = 'H'
                elif pScore < 12:
                    action = 'D'
                else:
                    action = 'St'
            else:
                # dealer holding 7-A
                if pScore < 17:
                    action = 'H'
                else:
                    action = 'St'
    return action


def sim_dealer_action(cards):
    '''
    Simulates decision for dealer
    '''
    if score(cards) < 17:
        action = 'H'
    else:
        action = 'St'
    return action


def calc_result(cards, dealer_score):
    '''
    Compares current hand (defined by cards) to dealer_score
        and deduct win/loss specified by bet
    '''
    result = ''
    if score(cards) > 21:
        # player busts
        result = 'L'
    else:
        # player does not bust
        if dealer_score > 21:
            # dealer busts
            result = 'W'
        else:
            # both player and dealer don't bust
            if (score(cards) > dealer_score):
                # player has higher score
                result = 'W'
            elif (score(cards) < dealer_score):
                # dealer has higher score
                result = 'L'
            else:
                result = 'B'
    return result
