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
        self.num_decks = num_decks
        self.size = num_decks*52
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*self.num_decks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*self.num_decks)
        random.shuffle(self.cards)
        # initialize state variables
        self.count = 0
        self.numHiRem = 16*self.num_decks # number of high cards remaining
        self.numAceRem = 4*self.num_decks # number of aces remaining

    def shuffle(self):
        '''
        Create new shuffled superdeck
        '''
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*self.num_decks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*self.num_decks)
        random.shuffle(self.cards)
        # reset state variables
        self.count = 0
        self.numHiRem = 16*self.num_decks # number of high cards remaining
        self.numAceRem = 4*self.num_decks # number of aces remaining

    def deal(self):
        card = self.cards.pop(0)
        # update state
        if card in ['J','Q','K',10]:
            self.count = self.count - 1
            self.numHiRem = self.numHiRem - 1
        elif card == 'A':
            self.count = self.count - 1
            self.numAceRem = self.numAceRem - 1
        elif (card > 1) & (card < 7):
            self.count = self.count + 1
        return card

    def compute(self):
        '''
        Calculates probability matrix based on current state of deck
        '''
        probHi = self.numHiRem/len(self.cards)
        probAce = self.numAceRem/len(self.cards)
