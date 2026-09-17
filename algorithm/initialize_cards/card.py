import json

with open('data/card_value.json',"r") as f:
    data = json.load(f)


class Card():
    def __init__(self,name,suit):
        self.name = name
        self.suit = suit
        self.value = data[name]
    def __repr__(self):
        return f"{self.name} of {self.suit}"
    def __eq__(self, other):
        if type(other) == int or type(other) == float:
            if self.value == other:
                return True
        if self.suit == other.suit and self.name == other.name:
            return True
        return False
    def __add__(self, other):
        return self.value+other.value
    def __sub__(self, other):
        return self.value - other.value
    def __lt__(self, other):
        return self.value < other.value
    def __gt__(self, other):
        return self.value > other.value

