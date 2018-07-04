#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:40:05 2017

@author: ronnyli
"""

import numpy as np
import pandas as pd

import sim21 as sim
import deckManager as dm

import pdb


class Player(object):
    '''
    Class object describing each player (incl dealer)
    '''

    def __init__(self, cash):
        self.cash = cash
        self.bet = 0 # current bet
        self.hands = [] # list of hands (each hand is a list)

    def reset(self):
        self.bet = 0
        self.hands = []

    def addCard(self, new_card, hand_num):
        if len(self.hands) == 0:
            # new hand
            self.hands.append({'cards':[new_card], 'done':False})
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
    GameDeck = dm.Deck(params['numDecks'])

    # create dict of Player instances
    Players = {}
    for n in range(0,params['numPlayers']-1):
        Players['P' + str(n+1)] = Player(params['playerCash'])
    Players[params['playerName']] = Player(params['playerCash'])
    Players['DEALER'] = Player(0)

    # START GAME
    play = True
    while play:

        # start of a new round - reset and prompt for bets
        for key in Players:
            Players[key].reset()
            if key == params['playerName']:
                if params['mode'] == 1:
                    # gameplay mode
                    bet = sim.query_bet(Players[key].cash, params['minBet'])
                else:
                    # simulation mode
                    bet = sim.sim_bet(Players[key].cash, params['minBet'])
                Players[key].bet = bet
            else:
                Players[key].bet = params['minBet']

        # check player bet
        if Players[params['playerName']].bet == 0:
            break

        # initial deal - 2 cards each
        for n in range(0,2):
            for key in Players:
                Players[key].addCard(GameDeck.deal(), 0)

        sim.display_cards(Players, True)
        pdb.set_trace()
        # loop all players and simulate decisions
        for key in Players:

            # Players[key].hands

            # keep looping as long as unfinished hands exist



            while (p.numHandsLeft() > 0):
                for handIdx in range(0,len(p.hands)):
                    if not p.hands[handIdx]['done']:
                        print(p.name + ', hand ' + str(handIdx))
                        if sim.score(p.hands[handIdx]['cards']) == 21:
                            print('Blackjack!')
                            p.hands[handIdx]['done'] = True
                        else:
                            # get action
                            if p.name == params['playerName']:
                                sim.display_cards(Players, False)
                                print('On hand ' + str(handIdx+1))
                                user_action = sim.query_action()
                            else:
                                user_action = sim.sim_action(p.hands[handIdx]['cards'])
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
                                hit = True
                                while 1:
                                    if hit:
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
                                        user_action = sim.query_action()
                                    else:
                                        user_action = sim.sim_action(p.hands[handIdx]['cards'])
                                    # process action
                                    if user_action == 'H':
                                        hit = True
                                    elif user_action in ['Sp','D']:
                                        print('ERROR - Cannot split or double down after hitting')
                                        hit = False
                                    else:
                                        # stay
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

        # pdb.set_trace()

    # print game summary
