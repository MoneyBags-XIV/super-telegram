class Object:
    def __init__(self, location, capacity=0, takable=False):
        self.location = location
        self.takable = takable
        self.capacity = capacity
    
    def set_location(self, new_location):
        index = self.location.contents.index(self)
        del self.location.contents[index]
        self.location = new_location
        self.location.contents.append(self)


class Item(Object):
    pass


class Room(Object):
    pass


class Player(Object):
    def __init__(self, location, contents, )