import pytest

from algorithm.initialize_cards.card import Card


def test_eq_against_matching_int():
    assert Card("Jack", "Spades") == 3


def test_eq_against_non_matching_int():
    assert not (Card("Jack", "Spades") == 5)


def test_eq_against_matching_float():
    assert Card("Ace", "Spades") == 1.1


def test_eq_against_non_matching_float():
    assert not (Card("Ace", "Spades") == 2.2)


def test_eq_against_equal_card():
    assert Card("Jack", "Spades") == Card("Jack", "Spades")


def test_eq_against_different_card():
    assert Card("Jack", "Spades") != Card("Jack", "Clubs")
    assert Card("Jack", "Spades") != Card("Queen", "Spades")


def test_eq_against_unrelated_type_does_not_raise():
    card = Card("Jack", "Spades")
    assert card != "Jack of Spades"
    assert card != None  # noqa: E711 - exercising __eq__ against None
    assert card != object()


def test_hash_allows_set_and_dict_membership():
    card = Card("Jack", "Spades")
    same = Card("Jack", "Spades")
    assert hash(card) == hash(same)
    assert card in {same}


def test_ordering_operators_use_rank():
    nine = Card("9", "Spades")
    ace = Card("Ace", "Spades")
    assert nine > ace
    assert ace < nine
    assert ace <= Card("Ace", "Clubs")
    assert nine >= Card("9", "Clubs")
