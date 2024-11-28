from tkinter import E
from typing_extensions import Self
from items import *
from not_the_parser import *

def create_game():

    game = Game("Test", 0)
    room = Room("Room", game, "This is a simple room.")
    bag = Item("Nationals Bag", room, "You got this bag from going to NB Nationals. Don't let anyone see the relay patch.", capacity=5, takable=True)
    item = Item("Nasty Knife", room, "This knife is pretty gnarly! Don't run with the point up.", takable=True)

    player = Player(room, 10, "You are looking magnificent today!")
    verb_list = create_verb_list(player)
    player.parser = Parser(player, game, verb_list)

    return game


def create_verb_list(player):

    ans = [
        Verb(['take', 'grab', 'pick up', 'steal', 'keep'], player, expects_direct=True, accepts_multiple_direct=True),
        Verb(['look', 'l', 'look around'], player)
    ]

    return ans