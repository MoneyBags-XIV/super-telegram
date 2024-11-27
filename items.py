from not_the_parser import Parser

class Object:
    def __init__(self, name, location, description, capacity=0, takable=False):
        self.location = location
        self.takable = takable
        self.capacity = capacity
        self.contents = []
        self.name = name
        self.description = description
        self.label = name.lower().replace(" ", "_")

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
        if len(new_location.contents) >= new_location.capacity and not type(new_location) is Room:
            return
        index = self.location.contents.index(self)
        del self.location.contents[index]
        self.location = new_location
        self.add_to_parent_contents()
    
    def do_turn(self):
        for x in self.contents:
            x.do_turn()


class Game(Object):
    def __init__(self, name, verbosity):
        super().__init__(name, False, '')
        self.verbosity = verbosity
        self.time = 0
    
    def do_turn(self):
        super().do_turn()
        self.time += 1


class Item(Object):
    pass


class Room(Object):
    def __init__(self, name, game, description):
        self.explored = False
        self.occupied = False
        
        super().__init__(name, game, description)
    
    def do_turn(self):
        print(self.describe())
        super().do_turn()
    
    def describe(self):
        ans = False
        for x in self.contents:
            if type(x) == Player:
                if not self.occupied:
                    ans = True
                self.occupied = True
                break
            self.occupied = False
        
        if ans:
            if not self.explored or self.game.verbosity > 0:
                return self.name + '\n' + self.description
            else:
                return self.name
        return ''
            


class Player(Object):

    def __init__(self, location, inventory_size, description):
        super().__init__("player", location, description, capacity=inventory_size)
        self.parser = Parser(self.game)
    
    def do_turn(self):
        ans = input("> ")
        self.parser.parse(ans)
        super().do_turn()
