# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 12:15:56 2017

Class for managing the deck and computing its state

@author: rli
"""

import random
import pdb

class Deck(object):
    '''
    '''

    def __init__(self, num_decks):
        self.numDecks = num_decks
        # initialize state variables in dictionary
        self.state = {'count':0, 'trueCount':0,
                        'numCardsPlayed':0,
                        'decksRem':self.numDecks,
                        'numHiRem':16*self.numDecks,
                        'numAceRem':4*self.numDecks,
                        'probHi':(16*self.numDecks)/(self.numDecks*52)}
        # Create new shuffled superdeck
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*self.numDecks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*self.numDecks)
        random.shuffle(self.cards)

    def shuffle(self):
        # reset state variables
        self.state['count'] = 0
        self.state['trueCount'] = 0
        self.state['numCardsPlayed'] = 0
        self.state['decksRem'] = self.numDecks
        self.state['numHiRem'] = 16*self.numDecks # number of high cards remaining
        self.state['numAceRem'] = 4*self.numDecks # number of aces remaining
        self.state['probHi'] = self.state['numHiRem']/self.state['cardsRem']
        # Create new shuffled superdeck
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*self.numDecks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*self.numDecks)
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop(0)
        self.state['numCardsPlayed'] = self.state['numCardsPlayed'] + 1
        self.state['decksRem'] = len(self.cards)/(self.numDecks*52)
        # update state
        if card in ['J','Q','K',10]:
            self.state['count'] = self.state['count'] - 1
            self.state['numHiRem'] = self.state['numHiRem'] - 1
        elif card == 'A':
            self.state['count'] = self.state['count'] - 1
            self.state['numAceRem'] = state['numAceRem'] - 1
        elif (card > 1) & (card < 7):
            self.state['count'] = self.state['count'] + 1
        self.state['probHi'] = self.state['numHiRem']/len(self.cards)
        return card
