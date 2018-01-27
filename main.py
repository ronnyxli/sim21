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

    # initialize figure to plot game flow on
    fig = plt.figure()
    plt.xlabel('True count')
    plt.ylabel('Prob(high card)')

    # START GAME
    play = True
    num_hands = 0
    while play:

        # restart
        for p in Players:
            p.reset()
            p.curr_bet = params['minBet']

        print(GameDeck.state)

        # save relevant parameters at beginning of round
        tc = GameDeck.state['trueCount']
        pHi = GameDeck.state['probHi']

        # prompt user for bet
        if (params['mode'] == 'play'):
            bet = sim.query_bet(Players[0].cash, params['minBet'])
        else:
            # bet double the minimum if count is above threshold
            if tc > 5:
                bet = 2*params['minBet']
            else:
                bet = params['minBet']
        if bet == 0:
            break
        else:
            Players[0].curr_bet = bet

        # initial deal: loop all rows and deal 2 cards to each player
        for n in range(0,2):
            for p in Players:
                p.addCard(GameDeck.deal(), 0)

        # check if dealer has blackjack
        if sim.score(Players[-1].hands[0]['cards']) == 21:
            print('Dealer has Blackjack')
            # display final hands
            sim.display_cards(Players, True)
            # loop other players and check if they have blackjack
            for p in Players[:-1]:
                if sim.score(p.hands[0]['cards']) == 21:
                    print('Bump on hand 1')
                    marker = 'b.'
                else:
                    p.cash = p.cash - p.hands[0]['bet']
                    print('You lost $' + str(p.hands[0]['bet']) + ' on hand 1')
                    marker = 'r.'
        else:
            # loop all players and simulate decisions
            for p in Players:
                # keep looping as long as unfinished hands exist
                while (p.numHandsLeft() > 0):
                    for handIdx in range(0,len(p.hands)):
                        if not p.hands[handIdx]['done']:
                            if sim.score(p.hands[handIdx]['cards']) == 21:
                                print('Blackjack!')
                                p.hands[handIdx]['done'] = True
                            else:
                                # get action
                                sim.display_cards(Players, False)
                                if (p.name == params['playerName']) & (params['mode'] == 'play'):
                                    # gameplay mode
                                    print('On hand ' + str(handIdx+1))
                                    action = sim.query_action(['H','St','Sp','D'])
                                elif (p.name == 'DEALER'):
                                    action = sim.sim_dealer_action(p.hands[handIdx]['cards'])
                                else:
                                    # simulation mode
                                    action = sim.sim_player_action(p.hands[handIdx]['cards'], \
                                                    Players[-1].hands[0]['cards'][0])
                                # process action
                                if action == 'Sp':
                                    split = p.split(handIdx)
                                    if split:
                                        # successful split - deal new cards to freshly split hands
                                        p.addCard(GameDeck.deal(), handIdx)
                                        p.addCard(GameDeck.deal(), handIdx+1)
                                    break
                                elif action == 'D':
                                    # double bet and give user one more card
                                    p.hands[handIdx]['bet'] = 2*p.hands[handIdx]['bet']
                                    p.addCard(GameDeck.deal(), handIdx)
                                    p.hands[handIdx]['done'] = True
                                elif action == 'H':
                                    while 1:
                                        p.addCard(GameDeck.deal(), handIdx)
                                        if sim.score(p.hands[handIdx]['cards']) > 21:
                                            if (p.name == params['playerName']) & (params['mode'] == 'play'):
                                                print('BUST')
                                            break
                                        else:
                                            # get action
                                            if (p.name == params['playerName']) & (params['mode'] == 'play'):
                                                # gameplay mode
                                                sim.display_cards(Players, False)
                                                print('On hand ' + str(handIdx+1))
                                                action = sim.query_action(['H','St','Sp','D'])
                                            elif (p.name == 'DEALER'):
                                                action = sim.sim_dealer_action(p.hands[handIdx]['cards'])
                                            else:
                                                # simulation mode
                                                action = sim.sim_player_action(p.hands[handIdx]['cards'], \
                                                                Players[-1].hands[0]['cards'][0])
                                        # process action
                                        if action == 'St':
                                            break
                                    p.hands[handIdx]['done'] = True
                                else:
                                    # stay
                                    p.hands[handIdx]['done'] = True

            # display final hands
            sim.display_cards(Players, True)

            # calculate results
            for p in Players[:-1]:
                # loop all hands
                for handIdx in range(0,len(p.hands)):
                    outcome = sim.calc_result(p.hands[handIdx]['cards'], \
                            sim.score(Players[-1].hands[0]['cards']))
                    if outcome == 'W':
                        p.cash = p.cash + p.hands[handIdx]['bet']
                        if p.name == params['playerName']:
                            print('You won $' + str(p.hands[handIdx]['bet']) + ' on hand ' + str(handIdx+1))
                            # update plot with beginning state and outcome of the round
                            plt.plot(tc, pHi, 'g.')
                    elif outcome == 'L':
                        p.cash = p.cash - p.hands[handIdx]['bet']
                        if p.name == params['playerName']:
                            print('You lost $' + str(p.hands[handIdx]['bet']) + ' on hand ' + str(handIdx+1))
                            plt.plot(tc, pHi, 'r.')
                    else:
                        print('Bump on hand ' + str(handIdx+1))
                        plt.plot(tc, pHi, 'b.')

        if p.cash == 0:
            print('Out of cash')
            play = False

        num_hands = num_hands + 1
        print(num_hands)
        if num_hands == params['maxHands']:
            play = False

        if GameDeck.state['decksRem'] < 0.5:
            GameDeck.shuffle()
            print('DECK SHUFFLED')

    # print game summary
    print('Final winnings = ' + str(Players[0].cash))
    plt.show()
    plt.close()
