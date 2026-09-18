from algorithm.game import Game
from algorithm.initialize_cards.card import Card


def make_game(trump=None, digged=False):
    game = Game("Bid")
    if trump is not None:
        game.register_trump(trump)
    if digged:
        game.dig()
    return game


def test_highest_card_of_lead_suit_wins_with_no_trump():
    game = make_game()
    trick = [
        Card("9", "Spades"),
        Card("King", "Spades"),
        Card("7", "Clubs"),
    ]

    winner, index = game.evaluate_current_winner(trick)

    assert index == 0
    assert winner == Card("9", "Spades")


def test_off_suit_non_trump_card_can_never_win():
    game = make_game(trump="Hearts", digged=True)
    trick = [
        Card("7", "Spades"),
        Card("Jack", "Clubs"),  # huge value, but neither lead suit nor trump
    ]

    winner, index = game.evaluate_current_winner(trick)

    assert index == 0
    assert winner == Card("7", "Spades")


def test_trump_beats_lead_suit_once_digged():
    game = make_game(trump="Hearts", digged=True)
    trick = [
        Card("Jack", "Spades"),
        Card("7", "Hearts"),
    ]

    winner, index = game.evaluate_current_winner(trick)

    assert index == 1
    assert winner == Card("7", "Hearts")


def test_trump_does_not_count_before_dig():
    game = make_game(trump="Hearts", digged=False)
    trick = [
        Card("Jack", "Spades"),
        Card("Ace", "Hearts"),  # would-be trump, but not live yet
    ]

    winner, index = game.evaluate_current_winner(trick)

    assert index == 0
    assert winner == Card("Jack", "Spades")
    assert game.active_trump is None


def test_earliest_play_wins_an_exact_tie():
    game = make_game()
    trick = [
        Card("Jack", "Spades"),
        Card("Jack", "Spades"),
    ]

    winner, index = game.evaluate_current_winner(trick)

    assert index == 0


def test_is_winning_matches_evaluate_current_winner():
    game = make_game(trump="Hearts", digged=True)
    trick = [
        Card("7", "Spades"),
        Card("Ace", "Hearts"),
        Card("King", "Spades"),
    ]

    assert game.is_winning(trick, 1) is True
    assert game.is_winning(trick, 0) is False
    assert game.is_winning(trick, 2) is False
