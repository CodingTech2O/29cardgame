from initialize_cards import initialize_cards,take_input_from_user,display_output_to_user
from game import game

bots,player = initialize_cards()
game.state = "Playing"

while len(game.played_hands) < 32:
    