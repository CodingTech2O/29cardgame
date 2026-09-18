from algorithm.initialize_cards import initialize_cards,take_input_from_user,display_output_to_user,Bot,Player,Card
from algorithm.game import game, SUITS


def should_offer_dig(is_leading, suit_in_cards, is_digged):
    """Only offer the dig when genuinely void in the lead suit, not leading."""
    return not is_leading and not suit_in_cards and not is_digged


def main_game():
    bots, player = initialize_cards()
    game.state = "Playing"
    game.players = []
    last_hands = []

    for bot in bots:
        game.players.append(bot)

    game.players.append(player)

    for i in range(8):
        current_hand = []

        for p in game.players:
            if type(p) == Player:

                is_leading = len(current_hand) == 0
                lead_suit = current_hand[0].suit if not is_leading else None
                suit_in_cards = is_leading or any(
                    card.suit == lead_suit for card in player.cards
                )

                dig = None
                if should_offer_dig(is_leading, suit_in_cards, game.is_digged):
                    dig = take_input_from_user("Do you want to dig? Y/N: ",str)
                    if dig.lower() == "y":
                        display_output_to_user("Trump is" + game.dig())

                while True:
                    raw_card = take_input_from_user("Enter card to play: ",str)

                    if " of " not in raw_card:
                        display_output_to_user(
                            "Please enter a card as '<rank> of <suit>', e.g. 'Jack of Spades'."
                        )
                        continue

                    name, suit = raw_card.split(" of ", 1)

                    if suit not in SUITS:
                        display_output_to_user(f"'{suit}' is not a valid suit.")
                        continue

                    try:
                        player_card = Card(name, suit)
                    except KeyError:
                        display_output_to_user(f"'{name}' is not a valid rank.")
                        continue

                    if player_card not in player.cards:
                        display_output_to_user(f"{player_card} is not in your hand.")
                        continue

                    if (
                        dig and dig.lower() == "y" and game.is_digged
                        and player_card.suit != game.trump
                        and player.filter(player.cards, suit=game.trump)
                    ):
                        display_output_to_user("You must play trump suit card!")
                        continue

                    if not is_leading and suit_in_cards and player_card.suit != lead_suit:
                        display_output_to_user(
                            f"You must follow suit ({lead_suit}) since you have it."
                        )
                        continue

                    try:
                        card = p.play_card(player_card)
                        break
                    except ValueError:
                        display_output_to_user(
                            f"{player_card} is not in your hand. Enter a card from your hand."
                        )

            else:
                card = p.decide_card_to_play(
                    game,
                    current_hand,
                    last_hands
                )

                display_output_to_user(card)

            current_hand.append(card)
        game.decide_new_order(current_hand)
        game.play_hand(current_hand)
        display_output_to_user(player.cards)

        last_hands.append(current_hand)
    display_output_to_user(game.evaluate_round_winner())


if __name__ == "__main__":
    main_game()