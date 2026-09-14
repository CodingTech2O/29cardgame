import json

with open('data/card_value.json') as f:
    data = json.load(f)


class Player:
    def __init__(self,name, cards):
        self.name = name
        self.cards = cards
        self.values = [i.value for i in cards]
        self.made_trump= False
    def next_cards(self, cards):
        self.cards.extend(cards)
        self.values = [i.value for i in self.cards]
    def make_trump(self,trump):
        self.made_trump= True
        self.trump= trump
    def __repr__(self):
        return self.name