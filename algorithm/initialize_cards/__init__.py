import random
from algorithm.initialize_cards.card import Card
from algorithm.initialize_cards.bot import Bot
from algorithm.initialize_cards.player import Player

bots = None
player = None


def deal(cards, n=4):
    """Pop n random cards out of `cards` (mutated in place) and return them."""
    dealt = []
    for _ in range(n):
        a = random.randint(0, len(cards) - 1)
        dealt.append(cards.pop(a))
    return dealt
