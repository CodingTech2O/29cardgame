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

