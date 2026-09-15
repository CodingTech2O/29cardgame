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

    def evaluate_current_winner(self,cards):
        values = []
        for card in card:
            if self.trump:
                if card.suit == self.trump:
                    values.append(card.value+4)
                else: values.append(card.value)
            else:
                values.append(card.value)

        return list(cards,values)
        

    
    def decide_card_to_play(self,game, current_hand=[], last_hands=[]):

        # =========================
        # First Round
        # =========================
        if len(last_hands) == 0:

            if len(current_hand) == 0:

                if self.made_trump:

                    if self.check_if_card_in_cards("Jack", self.trump):

                        return self.play_card(Card("Jack", self.trump))

                    elif (
                        self.check_if_card_in_cards("9", self.trump)
                        or self.check_if_card_in_cards("10", self.trump)
                        or self.check_if_card_in_cards("Ace", self.trump)
                    ):

                        return self.play_card(
                            min(self.filter(self.cards, suit=self.trump))
                        )

                else:

                    temp_cards = [
                        card for card in self.cards
                        if card.name == "Jack"
                    ]

                    if temp_cards.__len__() != 0:

                        card_to_play = ""

                        prev_cards_of_suit = 100

                        for temp_card in temp_cards:

                            cards_of_suit = 0

                            for card in self.cards:
                                if card.suit == temp_card.suit:
                                    cards_of_suit += 1

                            if cards_of_suit < prev_cards_of_suit:
                                prev_cards_of_suit = cards_of_suit
                                card_to_play = temp_card

                        return self.play_card(card_to_play)

                    else:

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                self.cards,
                                mini=-1,
                                suit=suit
                            )

                            if len(temp_cards) == 0:
                                continue

                            elif (
                                self.check_any_card_in_cards(
                                    ["9", "Ace", "10"],
                                    suit
                                )
                                and len(temp_cards) <= 2
                            ):
                                continue

                            elif (
                                card_to_play is None
                                or min(temp_cards) < card_to_play
                            ):
                                card_to_play = min(temp_cards)

                        if card_to_play is None:

                            card_to_play = min(
                                self.filter(self.cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

            elif len(current_hand) == 1:
                card_played = current_hand[0]
                cards = self.filter(cards,suit=card_played.suit)

                if cards:
                    minimum_valued_card_value = 100

                    if card_played.name == "Jack":
                        for card in cards:
                            if card.value < minimum_valued_card_value:
                                minimum_valued_card_value = card.value
                                card_to_play = card

                        return self.play_card(card_to_play)

                    else:
                        for card in cards:
                            if card.name == "Jack":
                                return self.play_card(card)

                        for card in cards:
                            if card.value < minimum_valued_card_value:
                                minimum_valued_card_value = card.value
                                card_to_play = card

                        return self.play_card(card_to_play)

                else:
                    if card_played.value > 2:
                        self.trump = game.dig()
                        minimum_valued_card_value = 100
                        cards = self.filter(self.cards,suit=self.trump)

                        for card in cards:
                            if card.value < minimum_valued_card_value:
                                minimum_valued_card_value = card.value
                                card_to_play = card

                        return self.play_card(card_to_play)

                    else:
                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                self.cards,
                                mini=-1,
                                suit=suit
                            )

                            if len(temp_cards) == 0:
                                continue

                            elif (
                                self.check_any_card_in_cards(
                                    ["9", "Ace", "10"],
                                    suit
                                )
                                and len(temp_cards) <= 2
                            ):
                                continue

                            elif (
                                card_to_play is None
                                or min(temp_cards) < card_to_play
                            ):
                                card_to_play = min(temp_cards)

                        if card_to_play is None:

                            card_to_play = min(
                                self.filter(self.cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

            else:
                opponent_cards = [current_hand[0]]
                current_suit = current_hand[0].suit

                if len(current_hand) > 2:
                    opponent_cards.append(current_hand[2])

                teammate_card = current_hand[1]

                if max(self.evaluate_current_winner(current_hand)[1]) == teammate_card.value and teammate_card.suit == current_suit:

                    if teammate_card.name == "Jack":
                        cards_most_worth = max(self.filter(self.cards,suit=current_suit))

                        for card in self.cards:
                            if card.value == cards_most_worth:
                                return self.play_card(card)

                        cards = self.filter(self.cards,3,0)
                        cards = sorted(cards)
                        return self.play_card(cards[-1])

                    elif Card("Jack",current_suit) in self.cards:
                        for card in self.cards:
                            if card == Card("Jack",current_suit):
                                return self.play_card(card)

                    else:
                        cards_least_worth = min(self.filter(self.cards,suit=current_suit))

                        for card in self.cards:
                            if card.value == cards_least_worth:
                                return self.play_card(card)

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                self.cards,
                                mini=-1,
                                suit=suit
                            )

                            if len(temp_cards) == 0:
                                continue

                            elif (
                                self.check_any_card_in_cards(
                                    ["9", "Ace", "10"],
                                    suit
                                )
                                and len(temp_cards) <= 2
                            ):
                                continue

                            elif (
                                card_to_play is None
                                or min(temp_cards) < card_to_play
                            ):
                                card_to_play = min(temp_cards)

                        if card_to_play is None:

                            card_to_play = min(
                                self.filter(self.cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

                else:
                    check_trump = self.filter(self.cards,suit=self.trump)
                    if check_trump:
                        cards_of_suit = self.filter(self.cards,suit=current_suit)
                        if cards_of_suit:
                            for card in cards:
                                if card.value == min(cards_of_suit):
                                    return self.play_card(card)


                        else:
                            cards_least_worth = min(self.filter(self.cards,suit=current_suit))

                            for card in self.cards:
                                if card.value == cards_least_worth:
                                    return self.play_card(card)

                            suits = [
                                "Diamonds",
                                "Clubs",
                                "Spades",
                                "Hearts"
                            ]

                            card_to_play = None

                            for suit in suits:

                                temp_cards = self.filter(
                                    self.cards,
                                    mini=-1,
                                    suit=suit
                                )

                                if len(temp_cards) == 0:
                                    continue

                                elif (
                                    self.check_any_card_in_cards(
                                        ["9", "Ace", "10"],
                                        suit
                                    )
                                    and len(temp_cards) <= 2
                                ):
                                    continue

                                elif (
                                    card_to_play is None
                                    or min(temp_cards) < card_to_play
                                ):
                                    card_to_play = min(temp_cards)

                            if card_to_play is None:

                                card_to_play = min(
                                    self.filter(self.cards, mini=-1)
                                )

                            return self.play_card(card_to_play)

                    else:
                        if Card("Jack",current_suit) in self.cards:
                            for card in self.cards:
                                if card == Card("Jack",current_suit):
                                    return self.play_card(card)
                        else:
                            if cards_of_suit:
                                for card in cards:
                                    if card.value == min(cards_of_suit):
                                        return self.play_card(card)
                            
                            
                            else:
                                cards_least_worth = min(self.filter(self.cards,suit=current_suit))
                            
                                for card in self.cards:
                                    if card.value == cards_least_worth:
                                        return self.play_card(card)
                            
                                suits = [
                                    "Diamonds",
                                    "Clubs",
                                    "Spades",
                                    "Hearts"
                                ]
                            
                                card_to_play = None
                            
                                for suit in suits:
                            
                                    temp_cards = self.filter(
                                        self.cards,
                                        mini=-1,
                                        suit=suit
                                    )
                            
                                    if len(temp_cards) == 0:
                                        continue
                            
                                    elif (
                                        self.check_any_card_in_cards(
                                            ["9", "Ace", "10"],
                                            suit
                                        )
                                        and len(temp_cards) <= 2
                                    ):
                                        continue
                            
                                    elif (
                                        card_to_play is None
                                        or min(temp_cards) < card_to_play
                                    ):
                                        card_to_play = min(temp_cards)
                            
                                if card_to_play is None:
                            
                                    card_to_play = min(
                                        self.filter(self.cards, mini=-1)
                                    )
                            
                                return self.play_card(card_to_play)

                                
                                                        


                

            

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