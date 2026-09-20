import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_wtf import CSRFProtect

import algorithm.initialize_cards as ic_module
from algorithm.game import game
from algorithm.round_flow import play_game

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-key")
CSRFProtect(app)

_generator = None
_pending_event = None
_history = []
_replay = []

_PAUSE_TYPES = {
    "need_name", "need_bid", "need_trump", "need_dig_choice", "need_card", "round_result",
}

REPLAY_MS = {"human_played": 800, "bot_played": 2000, "trick_won": 1800}
_REPLAY_SCREENS = {"need_card", "need_dig_choice", "round_result"}


def _advance(send_value=None):
    global _pending_event, _replay
    _replay = []
    try:
        event = _generator.send(send_value)
    except StopIteration:
        _pending_event = {"type": "game_over"}
        return

    while event["type"] not in _PAUSE_TYPES:
        _history.append(event)
        _replay.append(event)
        try:
            event = _generator.send(None)
        except StopIteration:
            _pending_event = {"type": "game_over"}
            return

    _pending_event = event


def _replay_frames():
    if not _pending_event or _pending_event["type"] not in _REPLAY_SCREENS:
        return []

    frames, dug_trump = [], None
    for event in _replay:
        if event["type"] == "dug":
            dug_trump = event["trump"]
        elif event["type"] in REPLAY_MS:
            frames.append({**event, "ms": REPLAY_MS[event["type"]], "dug_trump": dug_trump})
            dug_trump = None
    return frames


@app.route("/")
def index():
    tricks_done = sum(1 for e in _history if e["type"] == "trick_won")
    last_trick = next((e for e in reversed(_history) if e["type"] == "trick_won"), None)
    contract = next((e for e in _history if e["type"] == "bid_won"), None)
    return render_template(
        "index.html",
        started=_generator is not None,
        pending=_pending_event,
        history=list(reversed(_history[-12:])),
        game=game,
        player=ic_module.player,
        trick_number=min(tricks_done + 1, 8),
        last_trick=last_trick,
        contract=contract,
        replay=_replay_frames(),
    )


@app.route("/new-game", methods=["POST"])
def new_game():
    global _generator, _history
    _generator = play_game()
    _history = []
    _advance(None)
    return redirect(url_for("index"))


@app.route("/name", methods=["POST"])
def submit_name():
    if _pending_event and _pending_event["type"] == "need_name":
        _advance(request.form.get("name", ""))
    return redirect(url_for("index"))


@app.route("/bid", methods=["POST"])
def submit_bid():
    if _pending_event and _pending_event["type"] == "need_bid":
        _advance(request.form.get("bid", ""))
    return redirect(url_for("index"))


@app.route("/trump", methods=["POST"])
def submit_trump():
    if _pending_event and _pending_event["type"] == "need_trump":
        _advance(request.form.get("trump", ""))
    return redirect(url_for("index"))


@app.route("/dig", methods=["POST"])
def submit_dig():
    if _pending_event and _pending_event["type"] == "need_dig_choice":
        _advance(request.form.get("choice", ""))
    return redirect(url_for("index"))


@app.route("/play-card", methods=["POST"])
def submit_card():
    if _pending_event and _pending_event["type"] == "need_card":
        _advance((request.form.get("name", ""), request.form.get("suit", "")))
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
