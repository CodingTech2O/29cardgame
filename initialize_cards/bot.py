import json
from initialize_cards.card import Card


with open("data/card_value.json") as f:
    data = json.load(f)


class Bot:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.values = [card.value for card in cards]
        self.made_trump = False
        self.trump = None

    def next_cards(self, cards):
        self.cards.extend(cards)
        self.values = [card.value for card in self.cards]

    def make_trump(self, trump):
        self.made_trump = True
        self.trump = trump

    def __repr__(self):
        return self.name

    def check_if_card_in_cards(self, card, suit):
        card = Card(card, suit)

        if card in self.cards:
            return True

        return False

    def check_any_card_in_cards(self, cards, suit):
        for card in cards:
            card = Card(card, suit)

            if card in self.cards:
                return True

        return False

    def pair_in_card(self):
        king = False
        queen = False

        for card in self.cards:
            if card.name.lower() == "king":
                king = True

            if card.name.lower() == "queen":
                queen = True

        return king and queen

    def filter(self, cards, maxi=100, mini=0, suit=None):
        temp_cards = []

        for card in cards:
            if mini < card.value < maxi:
                if suit is None or card.suit == suit:
                    temp_cards.append(card)

        return temp_cards

    def decide_card_to_play(self, current_hand=[],last_hands = []):
        #First Round, First Turn
        if len(last_hands) == 0:
            if len(current_hand) == 0:
                #If made Trump
                if self.made_trump:
                    #If Jack of trump
                    if self.check_if_card_in_cards("Jack",self.trump):
                        #Play Jack
                        self.play_card(Card("Jack",self.trump))    
                    #Check for cards with points
                    elif self.check_if_card_in_cards("9",self.trump) or self.check_if_card_in_cards("10",self.trump) or self.check_if_card_in_cards("Ace",self.trump):
                        #Play Lowest card of trump
                        self.play_card(min(self.filter(self.cards,suit=self.trump)))
                #If not made trump
                else:
                    temp_cards = [card for card in self.cards if card.name == "Jack"]
                    if temp_cards.__len__() != 0: 
                        card_to_play = ""
                        prev_cards_of_suit = 100
                        for temp_card in temp_cards:
                            cards_of_suit = 0
                            for card in self.cards:
                                if card.suit == temp_card.suit:
                                    cards_of_suit +=1
                            if cards_of_suit < prev_cards_of_suit:
                                prev_cards_of_suit = cards_of_suit
                                card_to_play = temp_card
                        self.play_card(temp_card)                       
                

    def play_card(self, card):

        for i in range(len(self.cards)):

            if card == self.cards[i]:

                played_card = self.cards.pop(i)

                # Keep values synchronized
                self.values = [
                    card.value for card in self.cards
                ]

                return played_card

        return None