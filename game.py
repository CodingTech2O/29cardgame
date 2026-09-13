import json
from initialize_cards.card import Card
class Game:
    def __init__(self,state):
        self.state = state
        with open('data/card_value.json', "r") as f:
                data = json.load(f)
        
        suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']
        
        cards = []
        for suit in suits:
            for name in data:
                cards.append(Card(name, suit))
        self.cards = cards
        self.all_cards = cards
        self.played_hands = []


    def register_trump(self,trump):
        self.trump = trump

    def dig(self):
        return self.trump

    def play_hand(self,hand):
        for h in hand:
            for i in range(self.cards):
                if self.cards[i] == h:
                       self.card.pop(i)
                       self.played_hands.append(self.cards[i])
        return self.played_hands[-1]    
    


game = Game("Bid")