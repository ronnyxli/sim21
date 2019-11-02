
'''
Functions for simulating blackjack gameplay
'''
import pdb

def deal(deck, num_cards):
    '''
    '''
    pdb.set_trace()
    return True

def query_bet(min_bet, max_bet):
    '''
    Query bet from user
    '''
    valid_bet = False
    while not valid_bet:
        bet = input('Enter your bet (must be between ' + str(min_bet) + ' and ' + str(max_bet) + ', or enter 0 to leaves): ')
        try:
            bet = int(bet)
            if bet < min_bet:
                print('Try again - minimum bet is ' + str(min_bet))
            elif bet > max_bet:
                print('Try again - maximum bet is ' + str(max_bet))
            else:
                valid_bet = True
        except:
            print('Try again - bet must be an integer')

    return bet


def sim_bet(min_bet, max_bet):
    '''
    '''
    return None


def query_action():
    '''
    Hit, sp
    '''
    action = 'H'
    return action


def sim_action():
    '''
    '''
    return None
