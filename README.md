# sim21

Simulate a blackjack game given a card-counting and betting scheme.

DISCLAIMER 1: This program does not intend to promote card counting in any capacity. Please be aware that casinos have the right to kick you for counting cards. Please gamble responsibly.
DISCLAIMER 2: I do not have a gambling problem, I just like arithmetic.

Required Python libraries: numpy, pandas, random, math

The goal is of the simulator is to maximize the expected winnings for any given hand, defined as the product of the hand's probability of winning and the amount risked.

Total expected winning = P(BJ)xBJ_PAYOUT + P(win)xBET

NOTE: The probability of an event occurring is denoted as P(event).

Throughout the game, the simulator must know 3 things:
1) Counting scheme - point system
2) Betting scheme - when to bet high and when to bet lows
3) State of the deck - number of high cards, number of aces, win probability, etc.
