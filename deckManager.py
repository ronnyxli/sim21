# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 12:15:56 2017

Class for managing the deck and computing its state

@author: rli
"""

import random

class Deck(object):
    '''
    '''

    def __init__(self, num_decks):
        # create deck as list of cards
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*num_decks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*num_decks)
        random.shuffle(self.cards)
        # TODO: initialize probability matrix

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop(0)
        # TODO: update state
        return card

    # methods to compute state, probability matrix, etc.
