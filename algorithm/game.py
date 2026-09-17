import json
from algorithm.initialize_cards.card import Card
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
        self.all_cards = list(cards)
        self.played_hands = []
        self.is_digged = False
        self.players = []


    def register_trump(self,trump):
        self.trump = trump

    def dig(self):
        self.is_digged = True
        return self.trump

    def play_hand(self, hand):
        for h in hand:
            for i, c in enumerate(self.cards):
                if c == h:
                    self.played_hands.append(self.cards.pop(i))
                    break
        return self.played_hands[-1]
    
    


game = Game("Bid")