#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:40:05 2017

@author: ronnyli
"""

import numpy as np
import pandas as pd
import random

import sim21 as sim
import cardCounter as cc

import pdb


def init_game():
    '''
    Set simulation parameters
        Returns: Shuffled deck as list, game GAME as dataframe
    '''
    # query user for inputs
    # player_name = input('What is your name? ')
    # min_bet = int(input('What is the minimum bet at this table? (10-100) '))
    # num_decks = int(input('How many decks are used? (1-8) '))
    # num_players = int(input('How many other players at the table? (0-4) '))
    # player_cash = int(input('How much cash are you throwing down? (100-2500) '))

    # dev mode
    player_name = 'Ronny'
    min_bet = 25
    num_decks = 2
    num_players = 2
    player_cash = 400

    # create DECK deck as list
    DECK = []
    for card in ['J','Q','K','A']:
        DECK = DECK + [card]*(4*num_decks)
    for n in range(2,11):
        DECK = DECK + [n]*(4*num_decks)
    random.shuffle(DECK)

    # create dataframe for current GAME
    columns = ['Hand', 'Score', 'Cash'] # list of columns
    index = [player_name] # list of indexes
    for p in range(0,num_players):
        index.append('Player ' + str(p+2))
    index.append('Dealer')
    GAME = pd.DataFrame(index=index, columns=columns)
    GAME = GAME.fillna(0) # fill with 0's instead of nan's
    GAME.loc["Dealer" , "Cash"] = 'Inf'
    GAME.loc[0:-1, "Cash"] = player_cash

    return GAME, DECK, min_bet, player_name



if __name__ == "__main__":

    # gather user inputs and initalize DECK
    GAME, DECK, min_bet, player_name = init_game()
    # TODO: class for GAME?

    play = True
    while play:

        # clear all hands
        for player in GAME.index:
            GAME.loc[player,'Hand'] = 0

        # prompt user for bet
        bet = sim.query_bet(GAME.iloc[0,2], min_bet)
        if bet == 0:
            break

        # loop all rows and deal 2 cards
        for n in range(0,2):
            for player in GAME.index:
                GAME = sim.deal(GAME, player, DECK.pop(0))
                # if (n == 1) and (player == 'Dealer'):
                    # TODO: conceal dealer's second card

        print(GAME)

        GAME = sim.query_action(GAME, DECK, player_name)

        # TODO: play out hands for other players and dealer

        GAME = sim.calc_scores(GAME, player_name)

        print(GAME)
