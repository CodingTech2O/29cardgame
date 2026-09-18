import json
from algorithm.initialize_cards.helpers import take_input_from_user,display_output_to_user
from algorithm.game import game


with open("data/card_value.json", "r") as f:
    data = json.load(f)

suits = ['Spades', 'Clubs', 'Diamonds', 'Hearts']

MIN_BID = 17
PAIR_MIN_BID = 19


def get_strong_suit(bot):
    strong_suit = {}
    counts = {}
    for card in bot.cards:
        strong_suit[card.suit] = strong_suit.get(card.suit, 0) + 1.5 + card.value
        counts[card.suit] = counts.get(card.suit, 0) + 1

    # tie on score -> prefer the longer suit
    color = max(strong_suit, key=lambda s: (strong_suit[s], counts[s]))
    return [i for i in bot.cards if i.suit == color]


def pair_in_card(cards):
    king, queen = False, False
    for card in cards:
        if card.name.lower() == "king":
            king = True
        if card.name.lower() == "queen":
            queen = True
    return king and queen


def decide_bid(bot, last_bid=0):
    strong_suit = get_strong_suit(bot)
    strong_suit_points = sum([card.value for card in strong_suit])
    total_cards_points = sum([card.value for card in bot.cards])
    number_of_strong_suit_cards = len(strong_suit)

    possible_bid = []
    trump = strong_suit[0].suit
    has_pair = pair_in_card(strong_suit)

    ## No Bid ##
    if number_of_strong_suit_cards == 1 and total_cards_points < 6:
        return 0, 0
    elif number_of_strong_suit_cards == 2 and strong_suit_points < 3.5:
        return 0, 0
    elif number_of_strong_suit_cards == 3 and strong_suit_points < 2.5:
        return 0, 0

    ## Pair Bids (King + Queen of the strong suit) ##
    elif number_of_strong_suit_cards == 2 and has_pair:
        possible_bid = [i for i in range(PAIR_MIN_BID, 20)]
    elif number_of_strong_suit_cards == 3 and has_pair and strong_suit_points < 2:
        possible_bid = [i for i in range(PAIR_MIN_BID, 22)]
    elif number_of_strong_suit_cards == 3 and has_pair and strong_suit_points < 3:
        possible_bid = [i for i in range(PAIR_MIN_BID, 23)]
    elif number_of_strong_suit_cards == 3 and has_pair:
        possible_bid = [i for i in range(PAIR_MIN_BID, 24)]
    elif number_of_strong_suit_cards == 4 and has_pair and strong_suit_points < 1:
        possible_bid = [i for i in range(PAIR_MIN_BID, 22)]
    elif number_of_strong_suit_cards == 4 and has_pair and strong_suit_points < 2:
        possible_bid = [i for i in range(PAIR_MIN_BID, 23)]
    elif number_of_strong_suit_cards == 4 and has_pair and strong_suit_points < 3:
        possible_bid = [i for i in range(PAIR_MIN_BID, 24)]
    elif number_of_strong_suit_cards == 4 and has_pair and strong_suit_points < 5:
        possible_bid = [i for i in range(PAIR_MIN_BID, 25)]
    elif number_of_strong_suit_cards == 4 and has_pair:
        possible_bid = [i for i in range(PAIR_MIN_BID, 26)]

    ## Four-card trump ##
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 1:
        possible_bid = [i for i in range(PAIR_MIN_BID, 22)]
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 2:
        possible_bid = [i for i in range(MIN_BID, 18)]
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 3:
        possible_bid = [i for i in range(MIN_BID, 19)]
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 4:
        possible_bid = [i for i in range(MIN_BID, 19)]
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 5:
        possible_bid = [i for i in range(MIN_BID, 20)]
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 6:
        possible_bid = [i for i in range(MIN_BID, 21)]
    elif number_of_strong_suit_cards == 4 and strong_suit_points < 7:
        possible_bid = [i for i in range(MIN_BID, 22)]
    elif number_of_strong_suit_cards == 4:
        possible_bid = [i for i in range(MIN_BID, 23)]

    ## Three-card trump ##
    elif number_of_strong_suit_cards == 3 and strong_suit_points < 3:
        possible_bid = [i for i in range(MIN_BID, 18)]
    elif number_of_strong_suit_cards == 3 and strong_suit_points < 4:
        possible_bid = [i for i in range(MIN_BID, 19)]
    elif number_of_strong_suit_cards == 3 and strong_suit_points < 5:
        possible_bid = [i for i in range(MIN_BID, 20)]
    elif number_of_strong_suit_cards == 3 and strong_suit_points < 6:
        possible_bid = [i for i in range(MIN_BID, 21)]
    elif number_of_strong_suit_cards == 3:
        possible_bid = [i for i in range(MIN_BID, 22)]

    ## Two-card trump ##
    elif number_of_strong_suit_cards == 2 and strong_suit_points < 4:
        possible_bid = [i for i in range(MIN_BID, 18)]
    elif number_of_strong_suit_cards == 2 and strong_suit_points < 5:
        possible_bid = [i for i in range(MIN_BID, 19)]
    elif number_of_strong_suit_cards == 2:
        possible_bid = [i for i in range(MIN_BID, 20)]

    ## Flat hand (no real trump length) ##
    elif number_of_strong_suit_cards == 1 and total_cards_points < 8:
        possible_bid = [i for i in range(MIN_BID, 19)]
    elif number_of_strong_suit_cards == 1 and total_cards_points < 10:
        possible_bid = [i for i in range(MIN_BID, 20)]
    elif number_of_strong_suit_cards == 1:
        possible_bid = [i for i in range(MIN_BID, 21)]

    # a bid must beat the current one
    possible_bid = [b for b in possible_bid if b > last_bid]

    if len(possible_bid) == 0:
        return 0, 0
    else:
        return possible_bid[0], trump

def bid(p1_bid, p1_trump, p2_bid, p2_trump, p1, p2):

    # p1 passes
    if p1_bid == 0:
        return p2, p2_bid, p2_trump, True

    # p2 passes
    if p2_bid == 0:
        return p1, p1_bid, p1_trump, True

    # p1 wins
    if p1_bid > p2_bid:
        return p1, p1_bid, p1_trump, False

    # p2 wins
    if p2_bid > p1_bid:
        return p2, p2_bid, p2_trump, False

    # Tie -> p1 wins
    return p1, p1_bid, p1_trump, False

def do_bidding(b1, b2, b3, p1):

    # =========================
    # B1 vs B2
    # =========================

    b1_bid, b1_trump = decide_bid(b1)
    b2_bid, b2_trump = decide_bid(b2, b1_bid)

    while True:

        # B1
        new_b1_bid, new_b1_trump = decide_bid(b1, b2_bid)

        if new_b1_bid == 0:
            break

        b1_bid = new_b1_bid
        b1_trump = new_b1_trump

        # B2
        new_b2_bid, new_b2_trump = decide_bid(b2, b1_bid)

        if new_b2_bid == 0:
            break

        b2_bid = new_b2_bid
        b2_trump = new_b2_trump

    winner = bid(
        b1_bid,
        b1_trump,
        b2_bid,
        b2_trump,
        b1,
        b2
    )

    # =========================
    # Winner vs B3
    # =========================

    winner_player = winner[0]
    winner_bid = winner[1]
    winner_trump = winner[2]

    # B3 does NOT bid if B3 is teammate of winner
    if winner_player != b1:

        b3_bid, b3_trump = decide_bid(b3, winner_bid)

        while True:

            # Winner responds to B3
            new_winner_bid, new_winner_trump = decide_bid(
                winner_player,
                b3_bid
            )

            if new_winner_bid == 0:
                break

            winner_bid = new_winner_bid
            winner_trump = new_winner_trump

            # B3 responds
            new_b3_bid, new_b3_trump = decide_bid(
                b3,
                winner_bid
            )

            if new_b3_bid == 0:
                break

            b3_bid = new_b3_bid
            b3_trump = new_b3_trump

        winner = bid(
            winner_bid,
            winner_trump,
            b3_bid,
            b3_trump,
            winner_player,
            b3
        )

    # =========================
    # Winner vs P1
    # =========================

    winner_player = winner[0]
    winner_bid = winner[1]
    winner_trump = winner[2]

    # P1 can now CHOOSE to enter the bidding.
    # Passing means P1 does not reveal a bid and
    # the current winner keeps the contract.

    p1_bid = take_input_from_user(
        f"Your bid, must beat {winner_bid} from {winner_player}, pass = 0: ",
        int
    )

    if p1_bid == 0:
        winner = (
            winner_player,
            winner_bid,
            winner_trump
        )

    else:

        p1_trump = take_input_from_user(
            "Enter your trump: ",
            str
        )

        while p1_bid != 0:

            # Winner responds to P1
            new_winner_bid, new_winner_trump = decide_bid(
                winner_player,
                p1_bid
            )

            if new_winner_bid == 0:
                winner = (
                    p1,
                    p1_bid,
                    p1_trump
                )
                break

            winner_bid = new_winner_bid
            winner_trump = new_winner_trump

            # P1 responds
            p1_bid = take_input_from_user(
                f"Your bid, must beat {winner_bid}, pass = 0: ",
                int
            )

            if p1_bid == 0:
                winner = (
                    winner_player,
                    winner_bid,
                    winner_trump
                )
                break

            p1_trump = take_input_from_user(
                "Enter your trump: ",
                str
            )

    winner[0].make_trump(winner[2])
    game.register_trump(winner[2])

    return winner
