#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:40:05 2017

@author: ronnyli
"""

import numpy as np

import sim21 as sim
import deckManager

import pdb


class Player(object):
    '''
    Class object describing each player (incl dealer)
    '''

    def __init__(self, name, cash):
        self.name = name
        self.cash = cash
        self.curr_bet = 0
        self.hands = [] # list of hands (each hand is a dict)

    def reset(self):
        self.hands = []

    def addCard(self, new_card, hand_num):
        if not self.hands:
            # new hand
            self.hands.append({'cards':[new_card], 'bet':self.curr_bet, 'done':False})
        else:
            self.hands[hand_num]['cards'].append(new_card)

    def split(self, hand_num):
        '''
        Creates two hands out of the cards in the hand specified by hand_num
        '''
        pdb.set_trace()
        if hand_num < len(self.hands):
            if len(self.hands[hand_num]) == 2:
                card1 = self.hands[hand_num][0]
                card2 = self.hands[hand_num][1]
                if card1 == card2:
                    del self.hands[hand_num]
                    self.hands.append([card1])
                    self.hands.append([card2])
                else:
                    print('You may only split two of the same card')
            else:
                print('Must have two cards in the hand to split')
        else:
            print('Hand does not exist')



if __name__ == "__main__":

    # gather user inputs
    params = sim.init_game()

    # create instance of Deck class (described in deckManager.py)
    GameDeck = deckManager.Deck(params['numDecks'])

    # create list of Player instances
    Players = [] # empty list
    for n in range(0,params['numPlayers']-1):
        Players.append(Player('Player' + str(n+1), params['playerCash']))
    Players.append(Player(params['playerName'], params['playerCash']))
    Players.append(Player('DEALER', 0))

    # START GAME
    play = True
    while play:

        # restart
        for p in Players:
            p.reset()
            p.curr_bet = params['minBet']

        # prompt user for bet
        bet = sim.query_bet(Players[0].cash, params['minBet'])
        if bet == 0:
            break
        else:
            Players[0].curr_bet = bet

        # initial deal: loop all rows and deal 2 cards to each player
        for n in range(0,2):
            for p in Players:
                p.addCard(GameDeck.deal(), 0)

        # loop all positions and simulate decisions for all players
        for p in Players:
            if p.name == params['playerName']:
                for handIdx in range(0,len(p.hands)):
                    if sim.score(p.hands[handIdx]['cards']) == 21:
                        print('Blackjack!')
                    else:
                        sim.display_cards(Players, False)
                        print('On hand ' + str(handIdx))
                        user_action = sim.query_action()
                        if user_action == 'H':
                            while (user_action == 'H'):
                                p.addCard(GameDeck.deal(), handIdx)
                                sim.display_cards(Players, False)
                                print('On hand ' + str(handIdx))
                                user_action = sim.query_action()
                        elif user_action == 'D':
                            if len(p.hands[handIdx]['cards']) > 2:
                                print('Cannot double down after hitting')
                            else:
                                # double bet and give user one more card
                                p.hands[handIdx]['bet'] = 2*p.hands[handIdx]['bet']
                                p.addCard(GameDeck.deal(), handIdx)
                        elif user_action = 'Sp':
                            pdb.set_trace()
                        else: # stay
                            p.hands[handIdx]['done'] = True
            else:
                # simulate action for dealer and other players
                for handIdx in range(0,len(p.hands)):
                    while (sim.simAction(p.hands[handIdx]['cards'])) == 'H':
                        p.addCard(GameDeck.deal(), handIdx)

        # display final hands
        sim.display_cards(Players, True)

        # calculate results
        for p in Players:
            if p.name is not 'DEALER':
                result = sim.calc_results(p, sim.score(Players[-1].hands[0]['cards']))
                if p.name == params['playerName']:
                    print(result)
                    if p.cash == 0:
                        print('Out of cash')
                        play = False

    # print game summary
