import json
from algorithm.initialize_cards.card import Card
import math

CARD_VALUE_PATH = "data/card_value.json"

with open(CARD_VALUE_PATH) as f:
    data = json.load(f)

SUITS = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

# Set to True if your house rules make the trump suit live from the first
# trick instead of only after someone has dug for it.
TRUMP_LIVE_BEFORE_DIG = False


class Game:
    def __init__(self, state):
        self.state = state

        cards = []
        for suit in SUITS:
            for name in data:
                cards.append(Card(name, suit))

        self.cards = cards
        self.all_cards = list(cards)
        self.played_hands = []
        self.is_digged = False
        self.players = []
        self.itr = 0
        self.trump = None

    def register_trump(self, trump):
        self.trump = trump

    def dig(self):
        self.is_digged = True
        return self.trump

    @property
    def active_trump(self):
        """The trump suit as far as trick-taking is concerned.

        In 29 the trump is concealed at the start of the round and only
        starts beating the lead suit once it has been dug for.
        """
        if self.trump is None:
            return None
        if self.is_digged or TRUMP_LIVE_BEFORE_DIG:
            return self.trump
        return None

    def evaluate_current_winner(self, cards):
        """Return (winning_card, index_into_cards) for one trick.

        A card can only win if it follows the lead suit or is an active
        trump. Anything else is a discard and can never take the trick,
        however high its value.
        """
        if not cards:
            raise ValueError("cannot evaluate an empty trick")

        for position, card in enumerate(cards):
            if card is None:
                raise ValueError(
                    f"player at position {position} played no card"
                )

        lead_suit = cards[0].suit
        trump = self.active_trump

        best_index = None
        best_rank = None

        for index, card in enumerate(cards):
            if trump is not None and card.suit == trump:
                # trump beats every card of the lead suit
                rank = (1, card.value)
            elif card.suit == lead_suit:
                rank = (0, card.value)
            else:
                # a discard: not the lead suit, not trump
                continue

            # strictly greater, so the earliest play wins an exact tie
            if best_rank is None or rank > best_rank:
                best_rank = rank
                best_index = index

        # the lead card always follows its own suit, so this cannot be None
        return cards[best_index], best_index

    def is_winning(self, cards, index):
        """Whether cards[index] is currently the winning card of the trick."""
        _, winning_index = self.evaluate_current_winner(cards)
        return winning_index == index

    def evaluate_round_winner(self):
        making_player = None
        making_team = []
        opponent_team = []

        for i in range(len(self.players)):
            if self.players[i].made_trump:
                making_player = self.players[i]
                making_team = [self.players[i], self.players[(i + 2) % 4]]
                opponent_team = [
                    self.players[(i + 1) % 4],
                    self.players[(i + 3) % 4],
                ]
                break

        if making_player is None:
            raise RuntimeError("no player made trump for this round")

        ttl_pts = 0
        for player in making_team:
            if player.last_hand:
                ttl_pts += 1
            for hand in player.hands:
                for card in hand:
                    ttl_pts += card.points
        ttl_pts = math.floor(ttl_pts)
        if ttl_pts >= making_player.bid:
            return making_team
        return opponent_team

    def decide_new_order(self, hand):
        self.itr += 1
        current_winner, index = self.evaluate_current_winner(hand)
        self.players[index].hands.append(hand)

        if self.itr == 8:
            self.players[index].last_hand = True

        self.players = self.players[index:] + self.players[:index]
        return current_winner

    def play_hand(self, hand):
        for h in hand:
            for i, c in enumerate(self.cards):
                if c == h:
                    self.played_hands.append(self.cards.pop(i))
                    break
        return self.played_hands[-1]


game = Game("Bid")