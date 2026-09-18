import json
from algorithm.initialize_cards.card import Card
from algorithm.initialize_cards.helpers import display_output_to_user,take_input_from_user


with open("data/card_value.json") as f:
    data = json.load(f)


class Bot:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.values = [card.value for card in cards]
        self.made_trump = False
        self.trump = None
        self.hands =[]
        self.last_hand = False
        self.bid = None

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
        for card in cards:
            if self.trump:
                if card.suit == self.trump:
                    values.append(card.value+4)
                else: values.append(card.value)
            else:
                values.append(card.value)

        return list([cards,values])
        

    
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
                cards = self.filter(self.cards,suit=card_played.suit)

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
                        display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        minimum_valued_card_value = 100
                        cards = self.filter(self.cards,suit=self.trump)
                        card_to_play = None
                        for card in cards:
                            if card.value < minimum_valued_card_value:
                                minimum_valued_card_value = card.value
                                card_to_play = card
                        if card_to_play:
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
                        if self.filter(self.cards,suit=current_suit):
                            cards_most_worth = max(self.filter(self.cards,suit=current_suit))
                        

                        for card in self.filter(self.cards,suit=current_suit):
                            if card == cards_most_worth:
                                return self.play_card(card)

                        cards = self.filter(self.cards,3,0)
                        cards = sorted(cards)
                        return self.play_card(cards[-1])

                    elif Card("Jack",current_suit) in self.cards:
                        for card in self.cards:
                            if card == Card("Jack",current_suit):
                                return self.play_card(card)



                    else:
                        cards_least_worth = min(self.filter(self.cards,suit=current_suit),default=None)

                        for card in self.filter(self.cards,suit=current_suit):
                            if card == cards_least_worth:
                                return self.play_card(card)
                        if sum(current_hand) <= 3:
                            display_output_to_user("Trump is")
                            self.trump = display_output_to_user(game.dig())
                            cards = self.filter(self.cards,suit=self.trump)
                            if cards:
                                cards_with_min_value = min(cards)
                                for card in cards:
                                    if card.value == cards_with_min_value:
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
                    check_trump = self.filter(self.cards, suit=self.trump)

                    if check_trump:
                        cards_of_suit = self.filter(self.cards, suit=current_suit)

                        if cards_of_suit:
                            for card in cards_of_suit:
                                if card == min(cards_of_suit):
                                    return self.play_card(card)

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
                                card_to_play = min(self.filter(self.cards, mini=-1))

                            return self.play_card(card_to_play)

                    else:
                        cards_of_suit = self.filter(self.cards, suit=current_suit)

                        if Card("Jack", current_suit) in self.cards:
                            for card in self.cards:
                                if card == Card("Jack", current_suit):
                                    return self.play_card(card)

                        elif cards_of_suit:
                            for card in cards_of_suit:
                                if card == min(cards_of_suit):
                                    return self.play_card(card)

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
                                card_to_play = min(self.filter(self.cards, mini=-1))

                            return self.play_card(card_to_play)
        # =========================
        # Second round
        # =========================

        elif len(last_hands) == 1:
            if self.trump:
                trump_suit_cards_done = self.filter(game.played_hands, suit=self.trump)

                if trump_suit_cards_done:
                    for name in data:
                        if data[name] > max(card.value for card in trump_suit_cards_done) and Card(name, self.trump) in self.cards:
                            card_of_suit_most_worth = Card(name, self.trump)

                number_of_trump_cards_done = len(trump_suit_cards_done)
            try:
                if card_of_suit_most_worth:
                    highest_trump = True
            except:
                highest_trump = False
            if len(current_hand) == 0:

                last_game_suit = last_hands[0][0].suit
                temp_cards = [
                    card for card in self.cards
                    if card.name == "Jack" and card.suit != last_game_suit
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
                current_suit = current_hand[0].suit
                if current_suit == self.trump and highest_trump:
                    return self.play_card(card_of_suit_most_worth)
                
                elif self.check_if_card_in_cards("Jack",current_suit):
                    return self.play_card(Card("Jack", current_suit))
                else:
                    cards = self.filter(self.cards,suit=current_suit)
                    if cards:
                        cards_with_min_value = min(cards)
                        for card in cards:
                            if card == cards_with_min_value:
                                return self.play_card(card)
                    elif sum(current_hand) <= 3:
                        display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())
                        cards = self.filter(self.cards,suit=self.trump)
                        if cards:
                            cards_with_min_value = min(cards)
                            for card in cards:
                                if card == cards_with_min_value:
                                    return self.play_card(card)
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

                if max(self.evaluate_current_winner(current_hand)[1],default=0) == teammate_card.value and teammate_card.suit == current_suit:

                    if teammate_card.name == "Jack":
                        cards_most_worth = max(self.filter(self.cards,suit=current_suit),default=None)

                        for card in self.cards:
                            if card == cards_most_worth:
                                return self.play_card(card)

                        cards = self.filter(self.cards,3,0)
                        cards = sorted(cards)
                        return self.play_card(cards[-1])

                    elif Card("Jack",current_suit) in self.cards:
                        for card in self.cards:
                            if card == Card("Jack",current_suit):
                                return self.play_card(card)



                    else:
                        cards_least_worth = min(self.filter(self.cards,suit=current_suit),default=None)

                        for card in self.cards:
                            if card == cards_least_worth:
                                return self.play_card(card)
                        if sum(current_hand) <= 3:
                            display_output_to_user("Trump is")
                            self.trump = display_output_to_user(game.dig())
                            cards = self.filter(self.cards,suit=self.trump)
                            if cards:
                                cards_with_min_value = min(cards)
                                for card in cards:
                                    if card == cards_with_min_value:
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
                    check_trump = self.filter(self.cards, suit=self.trump)

                    if check_trump:
                        cards_of_suit = self.filter(self.cards, suit=current_suit)

                        if cards_of_suit:
                            for card in cards_of_suit:
                                if card == min(cards_of_suit):
                                    return self.play_card(card)

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
                                card_to_play = min(self.filter(self.cards, mini=-1))

                            return self.play_card(card_to_play)

                    else:
                        cards_of_suit = self.filter(self.cards, suit=current_suit)

                        if Card("Jack", current_suit) in self.cards:
                            for card in self.cards:
                                if card == Card("Jack", current_suit):
                                    return self.play_card(card)

                        elif cards_of_suit:
                            for card in cards_of_suit:
                                if card == min(cards_of_suit):
                                    return self.play_card(card)

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
                                card_to_play = min(self.filter(self.cards, mini=-1))

                            return self.play_card(card_to_play)


        # =========================
        # Third round
        # =========================

        elif len(last_hands) == 2:

            card_of_suit_most_worth = None
            highest_trump = False

            if self.trump:

                trump_suit_cards_done = self.filter(
                    game.played_hands,
                    mini=-1,
                    suit=self.trump
                )

                if len(trump_suit_cards_done) != 0:

                    for name in data:

                        if (
                            data[name] > max([card.value for card in trump_suit_cards_done],default=0)
                            and Card(name, self.trump) in self.cards
                        ):
                            card_of_suit_most_worth = Card(name, self.trump)

                number_of_trump_cards_done = len(trump_suit_cards_done)

            if card_of_suit_most_worth:
                highest_trump = True

            # -------------------------
            # the card kept back for the last hand
            # only a card that nothing can beat any more is worth keeping
            # -------------------------

            card_to_save = None

            for card in self.cards:

                card_is_sure = False

                if card.name == "Jack":
                    card_is_sure = True

                elif (
                    card.name == "9"
                    and Card("Jack", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                elif (
                    card.name == "Ace"
                    and Card("Jack", card.suit) in game.played_hands
                    and Card("9", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                elif (
                    card.name == "10"
                    and Card("Jack", card.suit) in game.played_hands
                    and Card("9", card.suit) in game.played_hands
                    and Card("Ace", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                if (
                    card_is_sure
                    and (
                        card_to_save is None
                        or card.value > card_to_save.value
                    )
                ):
                    card_to_save = card

            if card_to_save is None:

                usable_cards = self.cards

            else:

                usable_cards = [
                    card for card in self.cards
                    if card != card_to_save
                ]

                if len(usable_cards) == 0:
                    usable_cards = self.cards

            if len(current_hand) == 0:

                last_game_suits = [card.suit for card in last_hands[-1]]

                temp_cards = [
                    card for card in usable_cards
                    if card.name == "Jack" and card.suit not in last_game_suits
                ]

                if temp_cards.__len__() != 0:

                    card_to_play = ""

                    prev_cards_of_suit = 100

                    for temp_card in temp_cards:

                        cards_of_suit = 0

                        for card in usable_cards:
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
                            usable_cards,
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
                            self.filter(usable_cards, mini=-1)
                        )

                    return self.play_card(card_to_play)

            elif len(current_hand) == 1:

                current_suit = current_hand[0].suit

                # the saved card is given up when it is the only card of the suit
                if (
                    len(self.filter(usable_cards, mini=-1, suit=current_suit)) == 0
                    and len(self.filter(self.cards, mini=-1, suit=current_suit)) != 0
                ):
                    usable_cards = self.cards

                if (
                    current_suit == self.trump
                    and highest_trump
                    and card_of_suit_most_worth in usable_cards
                ):
                    return self.play_card(card_of_suit_most_worth)

                elif Card("Jack", current_suit) in usable_cards:
                    return self.play_card(Card("Jack", current_suit))

                else:

                    cards = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards:
                        return self.play_card(min(cards))

                    else:

                        if not self.trump and sum(current_hand) > 2:
                            display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        if self.trump:

                            cards = self.filter(usable_cards, mini=-1, suit=self.trump)

                            if cards:
                                return self.play_card(min(cards))

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                usable_cards,
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
                                self.filter(usable_cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

            else:

                opponent_cards = [current_hand[0]]
                current_suit = current_hand[0].suit

                if len(current_hand) > 2:
                    opponent_cards.append(current_hand[2])

                teammate_card = current_hand[1]

                if (
                    len(self.filter(usable_cards, mini=-1, suit=current_suit)) == 0
                    and len(self.filter(self.cards, mini=-1, suit=current_suit)) != 0
                ):
                    usable_cards = self.cards

                if max(self.evaluate_current_winner(current_hand)[1],default=0) == teammate_card.value and teammate_card.suit == current_suit:

                    cards = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards:
                        return self.play_card(max(cards))

                    cards = self.filter(usable_cards, 3, 0)

                    if cards:
                        cards = sorted(cards)
                        return self.play_card(cards[-1])

                    return self.play_card(
                        min(self.filter(usable_cards, mini=-1))
                    )

                else:

                    cards_of_suit = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards_of_suit:

                        if Card("Jack", current_suit) in usable_cards:
                            return self.play_card(Card("Jack", current_suit))

                        if max(cards_of_suit).value > max(self.evaluate_current_winner(current_hand)[1]):
                            return self.play_card(max(cards_of_suit))

                        return self.play_card(min(cards_of_suit))

                    else:

                        if not self.trump and sum(current_hand) > 2:
                            display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        if self.trump:

                            cards = self.filter(usable_cards, mini=-1, suit=self.trump)

                            if cards:
                                return self.play_card(min(cards))

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                usable_cards,
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
                                self.filter(usable_cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

        # =========================
        # Fourth hand
        # =========================

        elif len(last_hands) == 3:

            card_of_suit_most_worth = None
            highest_trump = False

            if self.trump:

                trump_suit_cards_done = self.filter(
                    game.played_hands,
                    mini=-1,
                    suit=self.trump
                )

                if len(trump_suit_cards_done) != 0:

                    for name in data:

                        if (
                            data[name] > max([card.value for card in trump_suit_cards_done])
                            and Card(name, self.trump) in self.cards
                        ):
                            card_of_suit_most_worth = Card(name, self.trump)

                number_of_trump_cards_done = len(trump_suit_cards_done)

            if card_of_suit_most_worth:
                highest_trump = True

            # -------------------------
            # the card kept back for the last hand
            # only a card that nothing can beat any more is worth keeping
            # -------------------------

            card_to_save = None

            for card in self.cards:

                card_is_sure = False

                if card.name == "Jack":
                    card_is_sure = True

                elif (
                    card.name == "9"
                    and Card("Jack", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                elif (
                    card.name == "Ace"
                    and Card("Jack", card.suit) in game.played_hands
                    and Card("9", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                elif (
                    card.name == "10"
                    and Card("Jack", card.suit) in game.played_hands
                    and Card("9", card.suit) in game.played_hands
                    and Card("Ace", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                if (
                    card_is_sure
                    and (
                        card_to_save is None
                        or card.value > card_to_save.value
                    )
                ):
                    card_to_save = card

            if card_to_save is None:

                usable_cards = self.cards

            else:

                usable_cards = [
                    card for card in self.cards
                    if card != card_to_save
                ]

                if len(usable_cards) == 0:
                    usable_cards = self.cards

            if len(current_hand) == 0:

                last_game_suits = [card.suit for card in last_hands[-1]]

                temp_cards = [
                    card for card in usable_cards
                    if card.name == "Jack" and card.suit not in last_game_suits
                ]

                if temp_cards.__len__() != 0:

                    card_to_play = ""

                    prev_cards_of_suit = 100

                    for temp_card in temp_cards:

                        cards_of_suit = 0

                        for card in usable_cards:
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
                            usable_cards,
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
                            self.filter(usable_cards, mini=-1)
                        )

                    return self.play_card(card_to_play)

            elif len(current_hand) == 1:

                current_suit = current_hand[0].suit

                # the saved card is given up when it is the only card of the suit
                if (
                    len(self.filter(usable_cards, mini=-1, suit=current_suit)) == 0
                    and len(self.filter(self.cards, mini=-1, suit=current_suit)) != 0
                ):
                    usable_cards = self.cards

                if (
                    current_suit == self.trump
                    and highest_trump
                    and card_of_suit_most_worth in usable_cards
                ):
                    return self.play_card(card_of_suit_most_worth)

                elif Card("Jack", current_suit) in usable_cards:
                    return self.play_card(Card("Jack", current_suit))

                else:

                    cards = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards:
                        return self.play_card(min(cards))

                    else:

                        if not self.trump and sum(current_hand) > 2:
                            display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        if self.trump:

                            cards = self.filter(usable_cards, mini=-1, suit=self.trump)

                            if cards:
                                return self.play_card(min(cards))

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                usable_cards,
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
                                self.filter(usable_cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

            else:

                opponent_cards = [current_hand[0]]
                current_suit = current_hand[0].suit

                if len(current_hand) > 2:
                    opponent_cards.append(current_hand[2])

                teammate_card = current_hand[1]

                if (
                    len(self.filter(usable_cards, mini=-1, suit=current_suit)) == 0
                    and len(self.filter(self.cards, mini=-1, suit=current_suit)) != 0
                ):
                    usable_cards = self.cards

                if max(self.evaluate_current_winner(current_hand)[1]) == teammate_card.value and teammate_card.suit == current_suit:

                    cards = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards:
                        return self.play_card(max(cards))

                    cards = self.filter(usable_cards, 3, 0)

                    if cards:
                        cards = sorted(cards)
                        return self.play_card(cards[-1])

                    return self.play_card(
                        min(self.filter(usable_cards, mini=-1))
                    )

                else:

                    cards_of_suit = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards_of_suit:

                        if Card("Jack", current_suit) in usable_cards:
                            return self.play_card(Card("Jack", current_suit))

                        if max(cards_of_suit).value > max(self.evaluate_current_winner(current_hand)[1]):
                            return self.play_card(max(cards_of_suit))

                        return self.play_card(min(cards_of_suit))

                    else:

                        if not self.trump and sum(current_hand) > 2:
                            display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        if self.trump:

                            cards = self.filter(usable_cards, mini=-1, suit=self.trump)

                            if cards:

                                trumps_in_hand = self.filter(
                                    current_hand,
                                    mini=-1,
                                    suit=self.trump
                                )

                                if trumps_in_hand:
                                    return self.play_card(max(cards))

                                return self.play_card(min(cards))

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                usable_cards,
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
                                self.filter(usable_cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

        # =========================
        # Fifth,Sixth,Seventh hand
        # =========================

        elif len(last_hands) == 4 or len(last_hands) == 5 or len(last_hands) == 6:

            if len(self.cards) == 1:
                return self.play_card(self.cards[0])

            card_of_suit_most_worth = None
            highest_trump = False

            if self.trump:

                trump_suit_cards_done = self.filter(
                    game.played_hands,
                    mini=-1,
                    suit=self.trump
                )

                if len(trump_suit_cards_done) != 0:

                    for name in data:

                        if (
                            data[name] > max([card.value for card in trump_suit_cards_done])
                            and Card(name, self.trump) in self.cards
                        ):
                            card_of_suit_most_worth = Card(name, self.trump)

                number_of_trump_cards_done = len(trump_suit_cards_done)

            if card_of_suit_most_worth:
                highest_trump = True

            # -------------------------
            # the card kept back for the last hand
            # only a card that nothing can beat any more is worth keeping,
            # and only when something else is left to play instead
            # -------------------------

            card_to_save = None

            for card in self.cards:

                card_is_sure = False

                if card.name == "Jack":
                    card_is_sure = True

                elif (
                    card.name == "9"
                    and Card("Jack", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                elif (
                    card.name == "Ace"
                    and Card("Jack", card.suit) in game.played_hands
                    and Card("9", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                elif (
                    card.name == "10"
                    and Card("Jack", card.suit) in game.played_hands
                    and Card("9", card.suit) in game.played_hands
                    and Card("Ace", card.suit) in game.played_hands
                ):
                    card_is_sure = True

                if (
                    card_is_sure
                    and (
                        card_to_save is None
                        or card.value > card_to_save.value
                    )
                ):
                    card_to_save = card

            if card_to_save is None:

                usable_cards = self.cards

            else:

                usable_cards = [
                    card for card in self.cards
                    if card != card_to_save
                ]

                if len(usable_cards) == 0:
                    usable_cards = self.cards

            if len(current_hand) == 0:

                last_game_suits = [card.suit for card in last_hands[-1]]

                temp_cards = [
                    card for card in usable_cards
                    if card.name == "Jack" and card.suit not in last_game_suits
                ]

                if temp_cards.__len__() != 0:

                    card_to_play = ""

                    prev_cards_of_suit = 100

                    for temp_card in temp_cards:

                        cards_of_suit = 0

                        for card in usable_cards:
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
                            usable_cards,
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
                            self.filter(usable_cards, mini=-1)
                        )

                    return self.play_card(card_to_play)

            elif len(current_hand) == 1:

                current_suit = current_hand[0].suit

                # the saved card is given up when it is the only card of the suit
                if (
                    len(self.filter(usable_cards, mini=-1, suit=current_suit)) == 0
                    and len(self.filter(self.cards, mini=-1, suit=current_suit)) != 0
                ):
                    usable_cards = self.cards

                if (
                    current_suit == self.trump
                    and highest_trump
                    and card_of_suit_most_worth in usable_cards
                ):
                    return self.play_card(card_of_suit_most_worth)

                elif Card("Jack", current_suit) in usable_cards:
                    return self.play_card(Card("Jack", current_suit))

                else:

                    cards = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards:
                        return self.play_card(min(cards))

                    else:

                        if not self.trump and sum(current_hand) > 2:
                            display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        if self.trump:

                            cards = self.filter(usable_cards, mini=-1, suit=self.trump)

                            if cards:
                                return self.play_card(min(cards))

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                usable_cards,
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
                                self.filter(usable_cards, mini=-1)
                            )

                        return self.play_card(card_to_play)

            else:

                opponent_cards = [current_hand[0]]
                current_suit = current_hand[0].suit

                if len(current_hand) > 2:
                    opponent_cards.append(current_hand[2])

                teammate_card = current_hand[1]

                if (
                    len(self.filter(usable_cards, mini=-1, suit=current_suit)) == 0
                    and len(self.filter(self.cards, mini=-1, suit=current_suit)) != 0
                ):
                    usable_cards = self.cards

                if max(self.evaluate_current_winner(current_hand)[1]) == teammate_card.value and teammate_card.suit == current_suit:

                    cards = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards:
                        return self.play_card(max(cards))

                    cards = self.filter(usable_cards, 3, 0)

                    if cards:
                        cards = sorted(cards)
                        return self.play_card(cards[-1])

                    return self.play_card(
                        min(self.filter(usable_cards, mini=-1))
                    )

                else:

                    cards_of_suit = self.filter(usable_cards, mini=-1, suit=current_suit)

                    if cards_of_suit:

                        if Card("Jack", current_suit) in usable_cards:
                            return self.play_card(Card("Jack", current_suit))

                        if max(cards_of_suit).value > max(self.evaluate_current_winner(current_hand)[1]):
                            return self.play_card(max(cards_of_suit))

                        return self.play_card(min(cards_of_suit))

                    else:

                        if not self.trump and sum(current_hand) > 2:
                            display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                        if self.trump:

                            cards = self.filter(usable_cards, mini=-1, suit=self.trump)

                            if cards:

                                trumps_in_hand = self.filter(
                                    current_hand,
                                    mini=-1,
                                    suit=self.trump
                                )

                                if trumps_in_hand:
                                    return self.play_card(max(cards))

                                return self.play_card(min(cards))

                        suits = [
                            "Diamonds",
                            "Clubs",
                            "Spades",
                            "Hearts"
                        ]

                        card_to_play = None

                        for suit in suits:

                            temp_cards = self.filter(
                                usable_cards,
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
                                self.filter(usable_cards, mini=-1)
                            )

                        return self.play_card(card_to_play)



        # =========================
        # Last hand
        # =========================

        else:

            if len(current_hand) == 0:

                temp_cards = [
                    card for card in self.cards
                    if card.name == "Jack"
                ]

                if temp_cards.__len__() != 0:
                    return self.play_card(max(temp_cards))

                if self.trump:

                    cards = self.filter(self.cards, mini=-1, suit=self.trump)

                    if cards:
                        return self.play_card(max(cards))

                return self.play_card(
                    max(self.filter(self.cards, mini=-1))
                )

            else:

                current_suit = current_hand[0].suit
                cards_of_suit = self.filter(self.cards, mini=-1, suit=current_suit)

                teammate_card = None

                if len(current_hand) > 1:
                    teammate_card = current_hand[1]

                if cards_of_suit:

                    if (
                        teammate_card
                        and max(self.evaluate_current_winner(current_hand)[1]) == teammate_card.value
                        and teammate_card.suit == current_suit
                    ):
                        return self.play_card(max(cards_of_suit))

                    if Card("Jack", current_suit) in self.cards:
                        return self.play_card(Card("Jack", current_suit))

                    if max(cards_of_suit).value > max(self.evaluate_current_winner(current_hand)[1]):
                        return self.play_card(max(cards_of_suit))

                    return self.play_card(min(cards_of_suit))

                else:

                    if not self.trump and sum(current_hand) > 2:
                        display_output_to_user("Trump is")
                        self.trump = display_output_to_user(game.dig())

                    if self.trump:

                        cards = self.filter(self.cards, mini=-1, suit=self.trump)

                        if cards:

                            trumps_in_hand = self.filter(
                                current_hand,
                                mini=-1,
                                suit=self.trump
                            )

                            if trumps_in_hand:
                                return self.play_card(max(cards))

                            return self.play_card(min(cards))

                    return self.play_card(
                        min(self.filter(self.cards, mini=-1))
                    )
                
    
    def play_card(self, card):

        for i in range(len(self.cards)):

            if card == self.cards[i]:

                played_card = self.cards.pop(i)

                # Keep values synchronized
                self.values = [card.value for card in self.cards]

                return played_card

        raise ValueError(f"{card} is not in hand: {self.cards}")
