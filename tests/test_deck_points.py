from algorithm.game import Game


def test_deck_totals_exactly_28_points():
    game = Game("Bid")

    assert len(game.all_cards) == 32
    assert sum(card.points for card in game.all_cards) == 28


def test_deck_points_plus_last_trick_bonus_is_29():
    game = Game("Bid")

    total = sum(card.points for card in game.all_cards)

    assert total + 1 == 29
