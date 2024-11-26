class Rooms:
    def __init__(self, adjacent_rooms, contents, description):
        self.adjacent_rooms = adjacent_rooms
        self.contents = contents
        self.description = description
    
    def __str__(self):
        return self.description