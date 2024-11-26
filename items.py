from parser import Parser

class Object:
    def __init__(self, location, capacity=0, contents=[], takable=False):
        self.location = location
        self.takable = takable
        self.capacity = capacity
        self.contents = contents

        self.game = self.set_game()

        if self.location:
            self.add_to_parent_contents()
    
    def add_to_parent_contents(self):
        self.location.contents.append(self)
    
    def set_game(self):
        ans = self
        while True:
            if type(ans) is Game:
                break
            ans = ans.location
        
        return ans
    
    def set_location(self, new_location):
        index = self.location.contents.index(self)
        del self.location.contents[index]
        self.location = new_location
        self.add_to_parent_contents()
    
    def do_turn(self):
        for x in self.contents:
            x.do_turn()


class Game(Object):
    def __init__(self, contents=[]):
        super().__init__(False, contents=contents)
    
    def do_turn(self):
        super().do_turn()
        self.time += 1


class Item(Object):
    pass


class Room(Object):
    pass


class Player(Object):

    def __init__(self, location, capacity=0, takable=False):
        super().__init__(location, capacity, takable)
        self.parser = Parser(2)
    
    def do_turn(self):
        ans = input("> ")
        self.parser.parse(ans)
