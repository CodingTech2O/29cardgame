import json
from algorithm.initialize_cards.card import Card

with open("data/card_value.json") as f:
    data = json.load(f)

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
        self.itr = 0
        self.trump = None

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
                elif cards[0].suit == card.suit:
                    values.append(card.value)
            elif cards[0].suit == card.suit:
                values.append(card.value)
        max_value = max(values)
        for i in range(len(values)):
            if values[i] == max_value:
                return cards[i],i
    def evaluate_round_winner(self):
        for i in range(len(self.players)):
            if self.players[i].made_trump and i%2 == 0:
                making_team = [self.players[0],self.players[2]]
                opponent_team = [self.players[1],self.players[3]]
                making_player = self.players[i]
            if self.players[i].made_trump and i%2 == 1:
                making_team = [self.players[1],self.players[3]]
                opponent_team = [self.players[0],self.players[2]]
                making_player = self.players[i]
        ttl_pts = 0
        for player in making_team:
            if player.last_hand:
                ttl_pts+=1
            for hand in player.hands:
                for card in hand:
                    ttl_pts+=card.value
        if ttl_pts >= making_player.bid:
            return making_team
        else:
            return opponent_team



    def decide_new_order(self,hand):
        self.itr+=1
        current_winner,index = self.evaluate_current_winner(hand)
        self.players[index].hands.append(hand)
        if self.itr == 8:
            self.players[index].last_hand = True
        self.players = self.players[index:] + self.players[:index]
    
    def play_hand(self, hand):
        for h in hand:
            for i, c in enumerate(self.cards):
                if c == h:
                    self.played_hands.append(self.cards.pop(i))
                    break
        return self.played_hands[-1]
    
    


game = Game("Bid")