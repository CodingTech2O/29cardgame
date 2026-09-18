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
    def evaluate_current_winner(self,cards):
        values = []
        for card in cards:
            if self.trump:
                if card.suit == self.trump:
                    values.append(card.value+4)
                else: values.append(card.value)
            else:
                values.append(card.value)
        max_value = max(values)
        for i in range(len(values)):
            if values[i] == max_value:
                return cards[i],i

    def decide_new_order(self,hand):
        current_winner,index = self.evaluate_current_winner(hand)
        self.players[index].hands.append(hand)
        self.players = self.players[index:] + self.players[:index]
    
    def play_hand(self, hand):
        for h in hand:
            for i, c in enumerate(self.cards):
                if c == h:
                    self.played_hands.append(self.cards.pop(i))
                    break
        return self.played_hands[-1]
    
    


game = Game("Bid")