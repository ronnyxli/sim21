#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:40:05 2017

@author: ronnyli
"""

import numpy as np
import matplotlib.pyplot as plt
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

    def numHandsLeft(self):
        '''
        Returns number of hands whose "done" value is False
        '''
        num_left = 0
        if self.hands:
            for hand in self.hands:
                if not hand['done']:
                    num_left = num_left + 1
        return num_left

    def split(self, hand_num):
        '''
        Creates two hands out of the cards in the hand specified by hand_num
        '''
        success = False # default
        if hand_num < len(self.hands):
            if len(self.hands[hand_num]['cards']) == 2:
                card1 = self.hands[hand_num]['cards'][0]
                card2 = self.hands[hand_num]['cards'][1]
                if card1 == card2:
                    # valid conditions for split
                    new_hand = {'cards':[card2], 'bet':self.curr_bet, 'done':False}
                    # insert new hand before the current one
                    self.hands.insert(hand_num, new_hand)
                    del self.hands[hand_num+1]['cards'][1]
                    success = True
                else:
                    print('ERROR - You may only split two of the same card')
            else:
                print('ERROR - Must have two cards in the hand to split')
        else:
            print('ERROR - Hand does not exist')
        return success



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
        print('Count = ' + str(GameDeck.state['count']))
        bet = sim.query_bet(Players[0].cash, params['minBet'])
        if bet == 0:
            break
        else:
            Players[0].curr_bet = bet

        # initial deal: loop all rows and deal 2 cards to each player
        for n in range(0,2):
            for p in Players:
                p.addCard(GameDeck.deal(), 0)

        # loop all players and simulate decisions
        for p in Players:
            # keep looping as long as unfinished hands exist
            while (p.numHandsLeft() > 0):
                for handIdx in range(0,len(p.hands)):
                    if not p.hands[handIdx]['done']:
                        # print(p.name + ', hand ' + str(handIdx))
                        if sim.score(p.hands[handIdx]['cards']) == 21:
                            print('Blackjack!')
                            p.hands[handIdx]['done'] = True
                        else:
                            # get action
                            if p.name == params['playerName']:
                                sim.display_cards(Players, False)
                                print('On hand ' + str(handIdx+1))
                                # TODO: print count?
                                user_action = sim.query_action(['H','St','Sp','D'])
                            else:
                                user_action = sim.simAction(p.hands[handIdx]['cards'])
                            # process action
                            if user_action == 'Sp':
                                split = p.split(handIdx)
                                if split:
                                    # successful split - deal new cards to freshly split hands
                                    p.addCard(GameDeck.deal(), handIdx)
                                    p.addCard(GameDeck.deal(), handIdx+1)
                                break
                            elif user_action == 'D':
                                # double bet and give user one more card
                                p.hands[handIdx]['bet'] = 2*p.hands[handIdx]['bet']
                                p.addCard(GameDeck.deal(), handIdx)
                                p.hands[handIdx]['done'] = True
                            elif user_action == 'H':
                                while 1:
                                    p.addCard(GameDeck.deal(), handIdx)
                                    if sim.score(p.hands[handIdx]['cards']) > 21:
                                        if p.name == params['playerName']:
                                            print('BUST')
                                        break
                                    else:
                                        if p.name == params['playerName']:
                                            sim.display_cards(Players, False)
                                    # get action
                                    if p.name == params['playerName']:
                                        print('On hand ' + str(handIdx+1))
                                        # TODO: print count?
                                        user_action = sim.query_action(['H','St'])
                                    else:
                                        user_action = sim.simAction(p.hands[handIdx]['cards'])
                                    # process action
                                    if user_action == 'St':
                                        break
                                p.hands[handIdx]['done'] = True
                            else:
                                # stay
                                p.hands[handIdx]['done'] = True

        # display final hands
        sim.display_cards(Players, True)

        # calculate results
        for p in Players:
            if p.name is not 'DEALER':
                # loop all hands
                net = 0
                for handIdx in range(0,len(p.hands)):
                    net = net + sim.calc_results(p.hands[handIdx]['cards'], \
                            p.hands[handIdx]['bet'], \
                            sim.score(Players[-1].hands[0]['cards']))
                    p.cash = p.cash + net
                    if p.name == params['playerName']:
                        if net > 0:
                            print('You won $' + str(np.abs(net)) + ' on hand ' + str(handIdx+1))
                        elif net < 0:
                            print('You lost $' + str(np.abs(net)) + ' on hand ' + str(handIdx+1))
                        else:
                            print('Bump on hand ' + str(handIdx+1))
                        if p.cash == 0:
                            print('Out of cash')
                            play = False

        if GameDeck.state['decksRem'] < 0.5:
            GameDeck.shuffle()
            print('DECK SHUFFLED')

        pdb.set_trace()

    # print game summary
