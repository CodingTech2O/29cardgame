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
        # First Round, First Turn
        # =========================
        if len(last_hands) == 0:

            # Check if no card has been played in the current hand
            if len(current_hand) == 0:

                # If made Trump
                if self.made_trump:

                    # If Jack of Trump
                    if self.check_if_card_in_cards("Jack", self.trump):

                        # Play Jack of Trump
                        return self.play_card(Card("Jack", self.trump))

                    # Check for cards with points
                    elif (
                        self.check_if_card_in_cards("9", self.trump)
                        or self.check_if_card_in_cards("10", self.trump)
                        or self.check_if_card_in_cards("Ace", self.trump)
                    ):

                        # Play Lowest Card of Trump
                        return self.play_card(
                            min(self.filter(self.cards, suit=self.trump))
                        )

                # If not made Trump
                else:

                    # Get all Jacks in hand
                    temp_cards = [
                        card for card in self.cards
                        if card.name == "Jack"
                    ]

                    # Check if there are any Jacks
                    if temp_cards.__len__() != 0:

                        # Store the card that should be played
                        card_to_play = ""

                        # Store the number of cards of the previously selected suit
                        prev_cards_of_suit = 100

                        # Check every Jack
                        for temp_card in temp_cards:

                            # Count cards of the Jack's suit
                            cards_of_suit = 0

                            # Count how many cards belong to this suit
                            for card in self.cards:
                                if card.suit == temp_card.suit:
                                    cards_of_suit += 1

                            # Select the Jack with the fewest cards of its suit
                            if cards_of_suit < prev_cards_of_suit:
                                prev_cards_of_suit = cards_of_suit
                                card_to_play = temp_card

                        # Play the selected Jack
                        return self.play_card(card_to_play)

                    # If no Jack is available

                    else:

                        # List of suits to check
                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        # Store the card that should be played
                        card_to_play = None

                        # Store the best suit based on number of cards
                        for suit in suits:

                            # Get the lowest card of this suit
                            temp_cards = self.filter(
                                self.cards,
                                mini=-1,
                                suit=suit
                            )

                            # Skip suit if there are no cards
                            if len(temp_cards) == 0:
                                continue

                            # Skip suit if it contains point cards
                            # and has 2 or fewer cards
                            elif (
                                self.check_any_card_in_cards(
                                    ["9", "Ace", "10"],
                                    suit
                                )
                                and len(temp_cards) <= 2
                            ):
                                continue

                            # Select the lowest card among the suits
                            elif (
                                card_to_play is None
                                or min(temp_cards) < card_to_play
                            ):
                                card_to_play = min(temp_cards)

                        # If no suitable card was found
                        if card_to_play is None:

                            # Play the lowest card in the hand
                            card_to_play = min(
                                self.filter(self.cards, mini=-1)
                            )

                        # Play the selected card
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
                        cards =  self.filter(self.cards,suit=self.trump)
                        
                        for card in cards:
                            if card.value < minimum_valued_card_value:
                                minimum_valued_card_value = card.value
                                card_to_play = card
                        return self.play_card(card_to_play)
                    else:
                        # List of suits to check
                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]
            
                        # Store the card that should be played
                        card_to_play = None
            
                        # Store the best suit based on number of cards
                        for suit in suits:
            
                            # Get the lowest card of this suit
                            temp_cards = self.filter(
                                self.cards,
                                mini=-1,
                                suit=suit
                            )
            
                            # Skip suit if there are no cards
                            if len(temp_cards) == 0:
                                continue
            
                            # Skip suit if it contains point cards
                            # and has 2 or fewer cards
                            elif (
                                self.check_any_card_in_cards(
                                    ["9", "Ace", "10"],
                                    suit
                                )
                                and len(temp_cards) <= 2
                            ):
                                continue
            
                            # Select the lowest card among the suits
                            elif (
                                card_to_play is None
                                or min(temp_cards) < card_to_play
                            ):
                                card_to_play = min(temp_cards)
            
                        # If no suitable card was found
                        if card_to_play is None:
            
                            # Play the lowest card in the hand
                            card_to_play = min(
                                self.filter(self.cards, mini=-1)
                            )
            
                        # Play the selected card
                        return self.play_card(card_to_play)
                
            else:
                opponent_cards = [current_hand[0]]

                if len(current_hand) > 2:
                    opponent_cards.append(current_hand[2])
                teammate_card = current_hand[1]

                if max(self.evaluate_current_winner(current_hand)[1]) == teammate_card.value:
                    pass
                else:
                    pass



                

            

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