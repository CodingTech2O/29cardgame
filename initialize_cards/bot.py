import json
from initialize_cards.card import Card


with open('data/card_value.json') as f:
    data = json.load(f)

class Bot:
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
    def check_if_card_in_cards(self,card,suit):
        card = Card(card,suit)
        if card in self.cards:
            return True 
        return False
    def check_any_card_in_cards(self,cards,suit):
        for card in cards:
            card = Card(card,suit)
            if card in self.cards:
                return True 
        return False
    def pair_in_card(cards):
        king, queen = False, False
        for card in cards:
            if card.name.lower() == "king":
                king = True
            if card.name.lower() == "queen":
                queen = True
        return king and queen

    def filter(self,cards,maxi=100,mini=0):
        temp_cards =[]
        for card in cards:
            if card <maxi and mini < card:
                temp_cards.append(card)
        

    def decide_card_to_play(self,current_hand:list=None):
        if len(current_hand) == 0:
            if self.made_trump:
                if self.check_if_card_in_cards("Jack",self.trump):
                    return Card("Jack",self.trump)
#                if self.check_any_card_in_cards(["7","8","K","Q"]) and not self.pair_in_card(self.cards) and self.check_if_card_in_cards("9",self.trump):
                    
                
    def play_card(self,card):
        for i in range(len(self.cards)):
            if card == self.cards[i]:
                self.cards.pop(i)

        return card
        
