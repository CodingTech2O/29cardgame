import json
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

def run_opening_auction(b1, b2):
    """Pure port of the B1-vs-B2 bid-off. Returns (winner, bid, trump, events)
    where events is every decide_bid() outcome in order, for narration."""
    events = []

    b1_bid, b1_trump = decide_bid(b1)
    events.append({"bidder": b1.name, "bid": b1_bid, "trump": b1_trump})
    b2_bid, b2_trump = decide_bid(b2, b1_bid)
    events.append({"bidder": b2.name, "bid": b2_bid, "trump": b2_trump})

    while True:
        new_b1_bid, new_b1_trump = decide_bid(b1, b2_bid)
        events.append({"bidder": b1.name, "bid": new_b1_bid, "trump": new_b1_trump})
        if new_b1_bid == 0:
            break
        b1_bid, b1_trump = new_b1_bid, new_b1_trump

        new_b2_bid, new_b2_trump = decide_bid(b2, b1_bid)
        events.append({"bidder": b2.name, "bid": new_b2_bid, "trump": new_b2_trump})
        if new_b2_bid == 0:
            break
        b2_bid, b2_trump = new_b2_bid, new_b2_trump

    winner, winner_bid, winner_trump, _ = bid(b1_bid, b1_trump, b2_bid, b2_trump, b1, b2)
    return winner, winner_bid, winner_trump, events


def run_challenger_auction(incumbent, incumbent_bid, incumbent_trump, challenger):
    """Pure port of the winner-vs-B3 bid-off. Returns (winner, bid, trump, events)."""
    events = []

    ch_bid, ch_trump = decide_bid(challenger, incumbent_bid)
    events.append({"bidder": challenger.name, "bid": ch_bid, "trump": ch_trump})

    while True:
        new_inc_bid, new_inc_trump = decide_bid(incumbent, ch_bid)
        events.append({"bidder": incumbent.name, "bid": new_inc_bid, "trump": new_inc_trump})
        if new_inc_bid == 0:
            break
        incumbent_bid, incumbent_trump = new_inc_bid, new_inc_trump

        new_ch_bid, new_ch_trump = decide_bid(challenger, incumbent_bid)
        events.append({"bidder": challenger.name, "bid": new_ch_bid, "trump": new_ch_trump})
        if new_ch_bid == 0:
            break
        ch_bid, ch_trump = new_ch_bid, new_ch_trump

    winner, winner_bid, winner_trump, _ = bid(
        incumbent_bid, incumbent_trump, ch_bid, ch_trump, incumbent, challenger
    )
    return winner, winner_bid, winner_trump, events
