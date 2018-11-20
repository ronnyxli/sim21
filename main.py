
import numpy as np
import random

import sim21 as sim

import pdb


class Deck(object):

    def __init__(self, num_decks):
        # create deck as list of cards
        self.cards = []
        for card in ['J','Q','K','A']:
            self.cards = self.cards + [card]*(4*num_decks)
        for n in range(2,11):
            self.cards = self.cards + [n]*(4*num_decks)
        random.shuffle(self.cards)
        # initialize dict for state variables
        self.state = {'numHi':16*num_decks, 'numAce':4*num_decks}

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop(0)
        # update state
        if card in ['J','Q','K',10]:
            self.state['numHi'] = self.state['numHi'] - 1
        elif card == 'A':
            self.state['numAce'] = self.state['numAce'] - 1
        return card

    def compute(self):
        '''
        Calculates probability matrix based on current state of deck
        '''
        probHi = self.state['numHi']/len(self.cards)
        probAce = self.state['numAce']/len(self.cards)



# TODO: recursive function to
def update_hands(hands, dealer_card):
    '''
    '''
    # call function until decision for all hands in St
    for hand in hands:

        # for each hand, get initial auto_decision
        decision = sim.auto_decision(hand, dealer_card)

        if decision == 'St':
            break
        else:
            if decision == 'H':
                hand.append(GameDeck.deal())
            elif decision == 'Sp':
                pdb.set_trace()
            elif decision == 'D':
                hand.append(GameDeck.deal())
                decision = 'St'
            pdb.set_trace()
            # call function until decision for all hands in St
            update_hands(hands, dealer_card)

    pdb.set_trace()
    return hands

if __name__ == "__main__":

    # gather user inputs and initialize list of players
    params, players = sim.init_game(True)

    # initialize deck
    GameDeck = Deck(params['numDecks'])

    # start simulation
    play = True
    while play:

        # simulate a round
        players = sim.query_bet(players, [params['minBet'],params['playerCash']])

        # initial deal - 2 cards per player
        for n in range(0,2):
            for p in range(0,len(players)):
                players[p]['Cards'][0].append(GameDeck.deal())

        sim.show_cards(players, True)

        # save dealer's up card
        dealer_idx = [x['Name'] for x in players].index('Dealer')
        dealer_up_card = players[dealer_idx]['Cards'][0][1]

        for p in range(0,len(players)):
            if players[p]['Name'] is not 'Dealer':
                curr_hands = players[p]['Cards']
                # call recursive function to update curr_hands
                new_hands = update_hands(curr_hands, dealer_up_card)
                pdb.set_trace()
                # replace with new hands
                players[p]['Cards'] = new_hands

        pdb.set_trace()

        sim.calc_results(players)

        sim.show_cards(players,False)

        pdb.set_trace()

    # TODO: display game summary
