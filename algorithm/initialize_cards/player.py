import json

with open('data/card_value.json') as f:
    data = json.load(f)


class Player:
    def __init__(self,name, cards):
        self.name = name
        self.cards = cards
        self.values = [i.value for i in cards]
        self.made_trump= False
        self.hands =[]
        self.last_hand = False
        self.bid = None

    def filter(self, cards, maxi=100, mini=0, suit=None):
        temp_cards = []

        for card in cards:
            if mini < card.value < maxi:
                if suit is None or card.suit == suit:
                    temp_cards.append(card)

        return temp_cards

    
    def next_cards(self, cards):
        self.cards.extend(cards)
        self.values = [i.value for i in self.cards]
    def make_trump(self,trump):
        self.made_trump= True
        self.trump= trump
        
    def play_card(self, card):

        for i in range(len(self.cards)):

            if card == self.cards[i]:

                played_card = self.cards.pop(i)

                # Keep values synchronized
                self.values = [card.value for card in self.cards]

                return played_card

        return None

    def __repr__(self):
        return self.name