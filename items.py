from not_the_parser import Parser

class Object:
    def __init__(self, name, location, description, capacity=0, takable=False, open=True):
        
        self.location = location if type(location) is list else [location]

        self.takable = takable
        self.capacity = capacity
        self.contents = []
        self.name = name
        self.description = description
        self.label = name.lower().replace(" ", "_")
        self.open = open

        self.game = self.set_game()

        if self.location:
            self.add_to_parent_contents()
    
    def add_to_parent_contents(self):
        for location in self.location:
            location.contents.append(self)
    
    def set_game(self):
        ans = self.location[0]
        while True:
            if type(ans) is Game:
                break
            ans = ans.location[0]
        
        return ans
    
    def set_location(self, new_locations):
        ans = []
        for new_location in new_locations:
            if len(new_location.contents) >= new_location.capacity and not type(new_location) is Room:
                continue
            ans.append(new_location)
        
        if not ans:
            return

        for x in self.location:
            index = self.location[x].contents.index(self)
            del self.location.contents[index]
        
        self.location = ans
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
        super().__init__(name, game, description)
    
    def do_turn(self):
        super().do_turn()
    
    def describe(self):
        if self.explored and self.game.verbosity == 0:
            return self.name
        return self.name + '\n' + self.description


class Player(Object):

    def __init__(self, location, inventory_size, description):
        super().__init__("player", location, description, capacity=inventory_size)
        self.parser = Parser(self.game)
    
    def do_turn(self):
        ans = input("> ")
        self.parser.parse(ans)
        super().do_turn()
    
    def can_touch(self, item):
        room = self.location

        ans = [item]
        new_ans = []

        while True:
            for x in ans:
                if type(ans) is Room:
                    new_ans.append(x)
                    continue
                for y in x.location:
                    if y.open:
                        new_ans.append(y)
            
            if ans == new_ans:
                break
            ans = new_ans
            new_ans = []
        
        for x in ans:
            if x == self.location[0]:
                return True
        return

        
