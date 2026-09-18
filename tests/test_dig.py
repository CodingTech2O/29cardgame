from algorithm import should_offer_dig


def test_dig_refused_when_leading_even_if_void_and_not_digged():
    # leading the trick means there is no lead suit to be void in yet;
    # this is the exact bug that offered the dig 13/67 times before the fix
    assert should_offer_dig(is_leading=True, suit_in_cards=False, is_digged=False) is False


def test_dig_refused_when_leading_regardless_of_other_flags():
    assert should_offer_dig(is_leading=True, suit_in_cards=True, is_digged=False) is False
    assert should_offer_dig(is_leading=True, suit_in_cards=False, is_digged=True) is False


def test_dig_refused_when_following_suit():
    assert should_offer_dig(is_leading=False, suit_in_cards=True, is_digged=False) is False


def test_dig_refused_once_already_digged():
    assert should_offer_dig(is_leading=False, suit_in_cards=False, is_digged=True) is False


def test_dig_offered_only_when_not_leading_and_void_and_not_digged():
    assert should_offer_dig(is_leading=False, suit_in_cards=False, is_digged=False) is True
