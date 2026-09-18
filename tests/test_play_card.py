import pytest

from algorithm.initialize_cards.bot import Bot
from algorithm.initialize_cards.card import Card
from algorithm.initialize_cards.player import Player


def test_player_play_card_removes_and_returns_matching_card():
    hand = [Card("Jack", "Spades"), Card("9", "Clubs")]
    player = Player("Adi", hand)

    played = player.play_card(Card("Jack", "Spades"))

    assert played == Card("Jack", "Spades")
    assert Card("Jack", "Spades") not in player.cards
    assert len(player.cards) == 1


def test_player_play_card_raises_on_card_not_in_hand():
    hand = [Card("Jack", "Spades"), Card("9", "Clubs")]
    player = Player("Adi", hand)

    with pytest.raises(ValueError):
        player.play_card(Card("Ace", "Hearts"))

    # the hand is untouched by the failed attempt
    assert len(player.cards) == 2


def test_bot_play_card_raises_on_card_not_in_hand():
    hand = [Card("Jack", "Spades"), Card("9", "Clubs")]
    bot = Bot("Bot1", hand)

    with pytest.raises(ValueError):
        bot.play_card(Card("Ace", "Hearts"))

    assert len(bot.cards) == 2
