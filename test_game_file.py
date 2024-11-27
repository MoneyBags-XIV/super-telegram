from items import *

def create_game():

    # synonyms_list = {
    #     "kill":["hit", "kick", ""]
    # }

    game = Game("Test", 0)
    room = Room("Room", game, "This is a simple room.")
    item = Item("Nasty Knife", room, "This knife is pretty gnarly! Never run with it.", takable=True)

    player = Player(room, 10, "You are looking magnificent today!")

    return game