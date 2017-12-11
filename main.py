#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:40:05 2017

@author: ronnyli
"""

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
        self.hand = [] # list of cards in player's hand

    def reset(self):
        self.hand = []

    def score(self):
        '''
        Calculate score of hand
        '''
        points = 0
        if len(self.hand) > 0:
            for card in self.hand:
                if card in ['J','Q','K']:
                    points = points + 10
                elif card == 'A':
                    points = points + 11
                else:
                    points = points + int(card)
        if ('A' in self.hand) & points > 21:
            points = points - 10
        return points

    def showHand(self, flag):
        if (self.name == 'DEALER') & (not flag):
            return [self.hand[0], '?']
        else:
            return self.hand

    def simAction(self):
        '''
        Simulates by-the-book decision for dealer and other players
        '''
        if self.score() < 17:
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

        # clear all hands
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
                p.hand.append(GameDeck.deal())

        # display initial hands
        sim.display_cards(Players, False)

        # handle user actions
        user_action = sim.query_action()
        if user_action == 'D':
            # double bet and give user one more card
            Players[0].curr_bet = Players[0].curr_bet*2
            Players[0].hand.append(GameDeck.deal())
            sim.display_cards(Players, 0)
        elif user_action == 'Sp':
            # TODO: handle split
            Players[0] = sim.handle_split(Players[0])
        else:
            while user_action == 'H':
                Players[0].hand.append(GameDeck.deal())
                sim.display_cards(Players, 0)
                if (Players[0].score()) > 21:
                    print('BUST')
                    break
                else:
                    user_action = sim.query_action()

        # simulate decisions for dealer and other players
        for p in Players[1:]:
            player_action = p.simAction()
            while player_action == 'H':
                p.hand.append(GameDeck.deal())
                player_action = p.simAction()

        sim.calc_results(Players)

        # print round summary
        sim.display_cards(Players, True)

        '''
        if results[0] == 'W':
            print('You won $' + str(Players[0].curr_bet))
            print('You have $' + )
        '''

        pdb.set_trace()

    # print game summary
