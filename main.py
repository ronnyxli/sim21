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
        self.hands = [] # list of hands (each hand is a list of cards)

    def reset(self):
        self.hands = []

    def addCard(self, new_card, hand_num):
        if not self.hands:
            self.hands.append([new_card])
        else:
            self.hands[hand_num].append(new_card)

    def split(self, hand_num):
        '''
        Creates two hands out of the cards in the hand specified by idx
        '''
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

    def simAction(self, hand_num):
        '''
        Simulates by-the-book decision for dealer and other players
        '''
        if sim.score(self.hands[hand_num]) < 17:
            action = 'H'
        else:
            action = 'St'
        return action



if __name__ == "__main__":

    # gather user inputs
    params = sim.init_game()

    # create instance of Deck class (described in deckManager.py)
    GameDeck = deckManager.Deck(params['numDecks'])

    # create list of Player instances
    Players = [Player(params['playerName'], params['playerCash'])]
    for n in range(0,params['numPlayers']-1):
        Players.append(Player('Player' + str(n+1), params['playerCash']))
    Players.append(Player('DEALER', 0))

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

        # display initial hands
        sim.display_cards(Players, False)

        # handle user action on each hands
        for idx in range(0,len(Players[0].hands)):
            print('On hand ' + str(idx+1))
            user_action = sim.query_action()
            if user_action == 'D':
                # double bet and give user one more card
                Players[0].curr_bet = Players[0].curr_bet*2
                Players[0].addCard(GameDeck.deal(), hand_num)
            elif user_action == 'Sp':
                Players[0].split(idx)
                pdb.set_trace()
            else:
                while user_action == 'H':
                    Players[0].addCard(GameDeck.deal(), idx)
                    sim.display_cards(Players, False)
                    if (sim.score(Players[0].hands[idx]) > 21):
                        break
                    else:
                        user_action = sim.query_action()

        # simulate decisions for dealer and other players
        for p in Players[1:]:
            for idx in range(0,len(p.hands)):
                while (p.simAction(idx) == 'H'):
                    p.addCard(GameDeck.deal(), idx)

        result = sim.calc_results(Players)

        # print round summary
        sim.display_cards(Players, True)

        print(result + '\n')

        pdb.set_trace()

        '''
        if results[0] == 'W':
            print('You won $' + str(Players[0].curr_bet))
            print('You have $' + )
        '''

    # print game summary
