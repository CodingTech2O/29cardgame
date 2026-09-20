from algorithm.game import game, SUITS
from algorithm.initialize_cards import deal, Bot, Player, Card
from algorithm.initialize_cards.bidding import decide_bid, run_opening_auction, run_challenger_auction
import algorithm.initialize_cards as ic_module


def should_offer_dig(is_leading, suit_in_cards, is_digged):
    """Only offer the dig when genuinely void in the lead suit, not leading."""
    return not is_leading and not suit_in_cards and not is_digged


def play_game():
    """Generator for one full round of 29.

    Yields a dict event at every step. Events whose "type" starts with
    "need_" (plus the terminal "round_result") pause the generator until
    .send(value) supplies a value matching that event's contract; an invalid
    value re-yields the same event with "error" set instead of advancing.
    All other events are informational and can be drained without pausing.
    The first .send() must be None.
    """
    game.reset()
    deck = game.build_full_deck()

    bot_hands = [deal(deck, 4) for _ in range(3)]
    player_hand = deal(deck, 4)

    name = yield from _ask_name()

    bots = [Bot(f"Bot{i + 1}", h) for i, h in enumerate(bot_hands)]
    player = Player(name, player_hand)
    ic_module.bots, ic_module.player = bots, player

    yield {"type": "hand_dealt", "hand": _hand_view(player), "phase": "initial"}

    b1, b2, b3 = bots
    winner, winner_bid, winner_trump, events = run_opening_auction(b1, b2)
    for e in events:
        yield {"type": "bot_bid", **e}

    if winner is not b1:
        winner, winner_bid, winner_trump, events = run_challenger_auction(
            winner, winner_bid, winner_trump, b3
        )
        for e in events:
            yield {"type": "bot_bid", **e}

    winner, winner_bid, winner_trump = yield from _human_bid_loop(
        winner, winner_bid, winner_trump, player
    )

    winner.bid = winner_bid
    winner.make_trump(winner_trump)
    game.register_trump(winner_trump)
    yield {
        "type": "bid_won",
        "winner": winner.name,
        "bid": winner_bid,
        "trump": winner_trump,
        "is_human": winner is player,
    }

    for b in bots:
        b.next_cards(deal(deck, 4))
    player.next_cards(deal(deck, 4))
    yield {"type": "hand_dealt", "hand": _hand_view(player), "phase": "final"}

    game.state = "Playing"
    game.players = [*bots, player]
    last_hands = []

    for trick_num in range(1, 9):
        current_hand = []
        for p in game.players:
            is_leading = len(current_hand) == 0
            lead_suit = current_hand[0].suit if not is_leading else None

            if isinstance(p, Player):
                suit_in_cards = is_leading or any(c.suit == lead_suit for c in p.cards)
                dug_this_turn = False
                if should_offer_dig(is_leading, suit_in_cards, game.is_digged):
                    wants_dig = yield from _ask_dig_choice(p, current_hand, lead_suit)
                    if wants_dig:
                        trump = game.dig()
                        dug_this_turn = True
                        yield {"type": "dug", "trump": trump}
                card = yield from _ask_card(
                    p, current_hand, lead_suit, is_leading, suit_in_cards, dug_this_turn
                )
                yield {
                    "type": "human_played",
                    "name": card.name,
                    "suit": card.suit,
                    "trick": _trick_view([*current_hand, card]),
                }
            else:
                was_digged = game.is_digged
                card = p.decide_card_to_play(game, current_hand, last_hands)
                if game.is_digged and not was_digged:
                    yield {"type": "dug", "trump": game.trump}
                yield {
                    "type": "bot_played",
                    "bot": p.name,
                    "name": card.name,
                    "suit": card.suit,
                    "trick": _trick_view([*current_hand, card]),
                }

            current_hand.append(card)

        trick_cards = _trick_view(current_hand)
        game.decide_new_order(current_hand)
        game.play_hand(current_hand)
        yield {
            "type": "trick_won",
            "trick_num": trick_num,
            "cards": trick_cards,
            "winner": game.players[0].name,
            "winner_seat": _seat(game.players[0]),
        }
        last_hands.append(current_hand)

    winners = game.evaluate_round_winner()
    yield {
        "type": "round_result",
        "winners": [pl.name for pl in winners],
        "making_player": winner.name,
        "bid": winner_bid,
        "trump": winner_trump,
        "made_it": winner in winners,
        "you_won": player in winners,
    }


def _ask_name():
    error = None
    while True:
        received = yield {"type": "need_name", "error": error}
        name = (received or "").strip()
        if not name:
            error = "Please enter a name."
            continue
        return name


def _ask_bid(to_beat, leader):
    error = None
    while True:
        received = yield {"type": "need_bid", "to_beat": to_beat, "leader": leader, "error": error}
        try:
            value = int(received)
        except (TypeError, ValueError):
            error = "Enter a whole number."
            continue
        if value != 0 and value <= to_beat:
            error = f"Your bid must be 0 (pass) or greater than {to_beat}."
            continue
        return value


def _ask_trump(bid_amount):
    error = None
    while True:
        received = yield {"type": "need_trump", "bid": bid_amount, "suits": SUITS, "error": error}
        if received not in SUITS:
            error = f"'{received}' is not a valid suit."
            continue
        return received


def _human_bid_loop(winner_player, winner_bid, winner_trump, human):
    p1_bid = yield from _ask_bid(winner_bid, winner_player.name)
    if p1_bid == 0:
        return winner_player, winner_bid, winner_trump

    p1_trump = yield from _ask_trump(p1_bid)
    while True:
        new_winner_bid, new_winner_trump = decide_bid(winner_player, p1_bid)
        if new_winner_bid == 0:
            return human, p1_bid, p1_trump

        winner_bid, winner_trump = new_winner_bid, new_winner_trump
        yield {"type": "bot_bid", "bidder": winner_player.name, "bid": winner_bid, "trump": winner_trump}

        p1_bid = yield from _ask_bid(winner_bid, winner_player.name)
        if p1_bid == 0:
            return winner_player, winner_bid, winner_trump

        p1_trump = yield from _ask_trump(p1_bid)


def _ask_dig_choice(player, current_hand, lead_suit):
    error = None
    while True:
        received = yield {
            "type": "need_dig_choice",
            "hand": _hand_view(player),
            "current_hand": _trick_view(current_hand),
            "lead_suit": lead_suit,
            "error": error,
        }
        choice = (received or "").strip().lower()
        if choice not in ("y", "n"):
            error = "Please choose Dig or Don't dig."
            continue
        return choice == "y"


def _ask_card(player, current_hand, lead_suit, is_leading, suit_in_cards, dug_this_turn):
    must_follow = not is_leading and suit_in_cards
    error = None
    while True:
        received = yield {
            "type": "need_card",
            "hand": _hand_view(player),
            "current_hand": _trick_view(current_hand),
            "lead_suit": lead_suit,
            "trump": game.active_trump,
            "must_follow_suit": must_follow,
            "error": error,
        }
        name, suit = received

        try:
            candidate = Card(name, suit)
        except KeyError:
            error = f"'{name}' is not a valid rank."
            continue

        if candidate not in player.cards:
            error = f"{candidate} is not in your hand."
            continue

        must_play_trump = (
            dug_this_turn
            and game.is_digged
            and candidate.suit != game.trump
            and player.filter(player.cards, suit=game.trump, mini=-1)
        )
        if must_play_trump:
            error = "You must play a trump suit card!"
            continue

        if must_follow and candidate.suit != lead_suit:
            error = f"You must follow suit ({lead_suit}) since you have it."
            continue

        return player.play_card(candidate)


def _hand_view(player):
    return [{"name": c.name, "suit": c.suit} for c in player.cards]


def _seat(p):
    return "you" if isinstance(p, Player) else p.name


def _trick_view(current_hand):
    return [{"player": p.name, "seat": _seat(p), "name": c.name, "suit": c.suit}
            for p, c in zip(game.players, current_hand)]
