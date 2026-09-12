class Game:
    def __init__(self,state):
        self.state = state

    def register_trump(self,trump):
        self.trump = trump

    def dig(self):
        return self.trump

game = Game("Bid")