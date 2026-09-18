"""Headless harness that plays N games of 29 by monkeypatching builtins.input.

Usage: python tests/harness.py [num_games] [base_seed]

For each game:
  - "Name: "             -> "Adi"
  - any "...bid..." bid  -> "0" (always pass; only bots contest trump)
  - "Do you want to dig" -> "n"
  - "Enter card to play" -> a legal card from the human's current hand,
        following the lead suit when the hand has one, chosen deterministically
        (first matching card) so games are reproducible from their seed.

`algorithm/__init__.py` defines a function named `initialize_cards`, which
shadows the submodule `algorithm.initialize_cards` on the `algorithm` package
object. To reach the *module* (and the `player`/`bots` globals it sets), look
it up in `sys.modules['algorithm.initialize_cards']` instead of attribute
access on the `algorithm` package.

`algorithm.game.game` is a module-level singleton, so every module under
`algorithm` is dropped from `sys.modules` and re-imported fresh for each game,
and `random` is reseeded per game so games are reproducible and independent.
"""
import builtins
import contextlib
import io
import os
import random
import sys
import traceback
from collections import Counter

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)


def _reset_algorithm_modules():
    for name in list(sys.modules):
        if name == "algorithm" or name.startswith("algorithm."):
            del sys.modules[name]


class FollowSuitViolation(Exception):
    pass


def _play_one_game(seed, quiet=True):
    """Play one full game headlessly. Returns (ok, error, violations)."""
    _reset_algorithm_modules()
    random.seed(seed)

    import algorithm  # noqa: F401  (re-imported fresh; registers submodules)

    ic_module = sys.modules["algorithm.initialize_cards"]
    player_module = sys.modules["algorithm.initialize_cards.player"]
    bot_module = sys.modules["algorithm.initialize_cards.bot"]
    game_module = sys.modules["algorithm.game"]

    trick = []  # cards played so far in the current trick, in play order
    violations = []  # (bot_name, card_played, lead_suit, hand_before_repr)

    orig_player_play = player_module.Player.play_card
    orig_bot_play = bot_module.Bot.play_card
    orig_play_hand = game_module.Game.play_hand

    def tracked_player_play(self, card):
        result = orig_player_play(self, card)
        trick.append(result)
        return result

    def tracked_bot_play(self, card):
        hand_before = list(self.cards)
        lead_suit = trick[0].suit if trick else None
        result = orig_bot_play(self, card)
        trick.append(result)

        if lead_suit is not None and result.suit != lead_suit:
            had_lead_suit = any(c.suit == lead_suit for c in hand_before)
            if had_lead_suit:
                violations.append(
                    (self.name, repr(result), lead_suit, [repr(c) for c in hand_before])
                )
        return result

    def tracked_play_hand(self, hand):
        result = orig_play_hand(self, hand)
        trick.clear()
        return result

    player_module.Player.play_card = tracked_player_play
    bot_module.Bot.play_card = tracked_bot_play
    game_module.Game.play_hand = tracked_play_hand

    def fake_input(prompt=""):
        p = str(prompt)
        pl = p.lower()
        if p.startswith("Name"):
            return "Adi"
        if "dig" in pl:
            return "n"
        if "enter card to play" in pl:
            hand = ic_module.player.cards
            if trick:
                lead_suit = trick[0].suit
                candidates = [c for c in hand if c.suit == lead_suit]
                if not candidates:
                    candidates = hand
            else:
                candidates = hand
            card = candidates[0]
            return f"{card.name} of {card.suit}"
        if "bid" in pl:
            return "0"
        if "trump" in pl:
            # unreachable in practice: the human always passes ("0" above),
            # so decide_bid/do_bidding never asks the human for a trump suit.
            return "Spades"
        raise AssertionError(f"harness has no canned answer for prompt: {p!r}")

    orig_input = builtins.input
    builtins.input = fake_input
    sink = io.StringIO()
    try:
        with contextlib.redirect_stdout(sink if quiet else sys.stdout):
            algorithm.main_game()
        return True, None, violations
    except Exception as exc:  # noqa: BLE001 - we want to classify *any* crash
        tb = traceback.extract_tb(exc.__traceback__)
        last = tb[-1] if tb else None
        location = f"{last.filename}:{last.lineno}" if last else "?"
        return False, (type(exc).__name__, str(exc), location), violations
    finally:
        builtins.input = orig_input


def run(num_games=200, base_seed=0, quiet=True):
    completed = 0
    crashes_by_type = Counter()
    crash_examples = {}
    total_violations = []
    total_bot_plays_estimate = 0

    for i in range(num_games):
        seed = base_seed + i
        ok, error, violations = _play_one_game(seed, quiet=quiet)
        total_violations.extend((seed,) + v for v in violations)
        total_bot_plays_estimate += 24  # 8 tricks x 3 bots, when a game completes

        if ok:
            completed += 1
        else:
            exc_type, msg, location = error
            key = f"{exc_type} @ {location}"
            crashes_by_type[key] += 1
            if key not in crash_examples:
                crash_examples[key] = (seed, msg)

    print(f"games completed: {completed}/{num_games}")
    print(f"crash rate: {(num_games - completed) / num_games:.1%}")
    if crashes_by_type:
        print("crashes by type @ originating line:")
        for key, count in crashes_by_type.most_common():
            seed, msg = crash_examples[key]
            print(f"  {count:4d}x  {key}  (e.g. seed={seed}: {msg})")
    else:
        print("no crashes")

    print(f"follow-suit violations by bots: {len(total_violations)}")
    for seed, name, card, lead_suit, hand_before in total_violations:
        print(f"  seed={seed} {name} played {card} (lead={lead_suit}) from hand {hand_before}")

    return completed, num_games, crashes_by_type, total_violations


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    seed = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    run(n, seed)
