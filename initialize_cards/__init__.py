from initialize_cards.card import Card
import json
import random
from initialize_cards.bot import Bot
from initialize_cards.player import Player
from initialize_cards.helpers import take_input_from_user,display_output_to_user
from initialize_cards.bidding import do_bidding



def initialize_cards():
    global bots,player
    with open('data/card_value.json', "r") as f:
        data = json.load(f)

    suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

    cards = []
    for suit in suits:
        for name in data:
            cards.append(Card(name, suit))

    bots = []
    for j in range(3):
        c = []
        for i in range(4):
            a = random.randint(0, len(cards) - 1)
            c.append(cards.pop(a))

        bots.append(Bot(f"Bot{j+1}",c))
    c = []
    for i in range(4):
        a = random.randint(0, len(cards) - 1)
        c.append(cards.pop(a))



    player = Player(take_input_from_user("Name: "), c)


    display_output_to_user(player.cards)
    bid = do_bidding(bots[0],bots[1],bots[2],player)

    display_output_to_user(f"{bid[0]} made trump at {bid[1]}")
    
    for bot in bots:
        c = []
        for i in range(4):
            a = random.randint(0, len(cards) - 1)
            c.append(cards.pop(a))
        bot.next_cards(c)
    c = []
    for i in range(4):
        a = random.randint(0, len(cards) - 1)
        c.append(cards.pop(a))
    player.next_cards(c)
    display_output_to_user(player.cards)
    return bots,player


