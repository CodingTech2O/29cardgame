from algorithm.initialize_cards import initialize_cards,take_input_from_user,display_output_to_user,Bot,Player,Card
from algorithm.game import game

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
                

                if len(current_hand) != 0:
                    suit_in_cards = False
                    for card in player.cards:
                        if card.suit == current_hand[0].suit:
                            suit_in_cards = True
                dig = None

                if not suit_in_cards:
                    if not game.is_digged:
                        dig = take_input_from_user("Do you want to dig? Y/N: ",str)
                        if dig.lower() == "y":
                            display_output_to_user("Trump is" + game.dig())


                player_card = take_input_from_user("Enter card to play: ",str)

                player_card = Card(
                    player_card.split(" of ")[0],
                    player_card.split(" of ")[1]
                )
                if dig and game.is_digged:
                    while dig.lower() == "y" and player_card.suit != game.trump and player.filter(player.cards,suit=game.trump):
                        display_output_to_user("You must play trump suit card!")
                        player_card = take_input_from_user("Enter card to play: ",str)

                        player_card = Card(
                            player_card.split(" of ")[0],
                            player_card.split(" of ")[1]
                        )


                while True:
                    try:
                        card = p.play_card(player_card)
                        break
                    except ValueError:
                        display_output_to_user(
                            f"{player_card} is not in your hand. Enter a card from your hand."
                        )
                        player_card = take_input_from_user("Enter card to play: ",str)

                        player_card = Card(
                            player_card.split(" of ")[0],
                            player_card.split(" of ")[1]
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