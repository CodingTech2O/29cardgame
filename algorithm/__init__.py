from algorithm.initialize_cards.helpers import take_input_from_user, display_output_to_user
from algorithm.round_flow import play_game, should_offer_dig


def _cli_prompt_for(event):
    t = event["type"]
    if t == "need_name":
        return take_input_from_user("Name: ", str)
    if t == "need_bid":
        return take_input_from_user(
            f"Your bid, must beat {event['to_beat']} from {event['leader']}, pass = 0: ", int
        )
    if t == "need_trump":
        return take_input_from_user("Enter your trump: ", str)
    if t == "need_dig_choice":
        return take_input_from_user("Do you want to dig? Y/N: ", str).strip().lower()
    if t == "need_card":
        while True:
            raw = take_input_from_user("Enter card to play: ", str)
            if " of " not in raw:
                display_output_to_user(
                    "Please enter a card as '<rank> of <suit>', e.g. 'Jack of Spades'."
                )
                continue
            name, suit = raw.split(" of ", 1)
            return (name, suit)
    raise AssertionError(f"no CLI handling for pause event type {t!r}")


def _narrate(event):
    t = event["type"]
    if t == "hand_dealt":
        display_output_to_user(", ".join(f"{c['name']} of {c['suit']}" for c in event["hand"]))
    elif t == "bot_bid":
        note = f" ({event['trump']})" if event["bid"] else ""
        display_output_to_user(f"{event['bidder']} bids {event['bid']}{note}")
    elif t == "bid_won":
        display_output_to_user(f"{event['winner']} made trump at {event['bid']}")
    elif t == "bot_played":
        display_output_to_user(f"{event['bot']} played {event['name']} of {event['suit']}")
    elif t == "dug":
        display_output_to_user(f"Trump is {event['trump']}")
    elif t == "trick_won":
        display_output_to_user(f"Trick {event['trick_num']} won by {event['winner']}")


def main_game():
    """Synchronous CLI driver over algorithm.round_flow.play_game()."""
    gen = play_game()
    value = None
    while True:
        try:
            event = gen.send(value)
        except StopIteration:
            return

        if event["type"] == "round_result":
            display_output_to_user(event["winners"])
            return

        if event["type"].startswith("need_"):
            if event.get("error"):
                display_output_to_user(event["error"])
            value = _cli_prompt_for(event)
        else:
            _narrate(event)
            value = None


if __name__ == "__main__":
    main_game()
