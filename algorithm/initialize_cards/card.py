import json

with open('data/card_value.json',"r") as f:
    data = json.load(f)

with open('data/card_points.json',"r") as f:
    points_data = json.load(f)


class Card():
    def __init__(self,name,suit):
        self.name = name
        self.suit = suit
        self.value = data[name]
        self.points = points_data[name]
    def __repr__(self):
        return f"{self.name} of {self.suit}"
    def __eq__(self, other):
        if isinstance(other, (int, float)):
            return self.value == other
        if isinstance(other, Card):
            return self.suit == other.suit and self.name == other.name
        return NotImplemented

    def __hash__(self):
        return hash((self.name, self.suit))

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return self.value + other
        return self.value + other.value

    def __radd__(self, other):
        return other + self.value

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self.value - other
        return self.value - other.value

    def __rsub__(self, other):
        return other - self.value
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value
    def __le__(self, other):
        return self.value <= other.value
    def __ge__(self, other):
        return self.value >= other.value

