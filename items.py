class Object:
    def __init__(self, name, location, description, synonyms=None, capacity=0, displayable=True, takable=False, open=True, conatainer=False):

        #TODO add functionality for pronouns (store and it)
        #TODO add way to store last command for redo
        
        self.location = location if type(location) is list else [location]

        self.takable = takable
        self.capacity = capacity
        self.contents = []
        self.name = name
        self.description = description
        self.label = name.lower().replace(" ", "_")
        self.open = open
        self.displayable = displayable
        self.container = conatainer

        self.synonyms = synonyms if synonyms else []
        self.synonyms.append(self.name)

        self.game = self.set_game()

        if self.location[0]:
            self.add_to_parent_contents()
    
    def add_to_parent_contents(self):
        for location in self.location:
            location.contents.append(self)
    
    def set_game(self):
        ans = self
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
            index = x.contents.index(self)
            del x.contents[index]
        
        self.location = ans
        self.add_to_parent_contents()

        return True
    
    def do_turn(self):
        for x in self.contents:
            x.do_turn()
    
    def describe(self):
        return self.description
    
    def find_object_by_name(self, object):
        for x in self.contents:
            lower = [i.lower() for i in x.synonyms]
            if object.lower() in lower:
                return x
        for x in self.contents:
            y = x.find_object_by_name(object)
            if y:
                return y
        return
    
    def formatted_contents(self, indent_depth=1):

        ans = ""

        for x in self.contents:
            if not x.displayable:
                continue
            
            prep = "An " if x.name in ['a', 'e', 'i', 'o', 'u'] else "A "
            indent = " " * indent_depth

            ans += (indent + prep + x.name + '\n')

            if x.container and x.open and x.contents:
                ans += (indent + "The " + x.name + " contains:\n")
                ans += (x.formatted_contents(indent_depth=indent_depth+1))
        
        return ans



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
        super().__init__(name, game, description, synonyms=['floor', 'ground'])
    
    def do_turn(self):
        super().do_turn()
    
    def describe(self):

        description = self.name + '\n' + self.description

        ans = self.formatted_contents()

        if not ans:
            return description
        
        ans = "You see here:\n" + ans

        ans = description + '\n' + ans
        return ans


class Player(Object):

    def __init__(self, location, inventory_size, description):
        super().__init__("me", location, description, capacity=inventory_size, displayable=False, synonyms=["myself", "i"])

        self.look(None, None, None)
    
    def do_turn(self):
        super().do_turn()

        # self.parser is assigned at the creation of the player instance. I forgot why I did this.
        verb, direct, indirect, used_verb = self.parser.parse()
        used_verb = used_verb[:1].upper() + used_verb[1:] + '.'
        verb(direct, indirect, used_verb)
    
    def take(self, direct, indirect, used_verb):
        
        for x in direct:
            if len(direct) > 1:
                print('(' + x.name + ')', end=' ')
            
            if not self.can_touch(x):
                print("You don't see any " + x.name + " here!")
                continue

            if x in self.contents:
                print("You are already holding that!")
                continue
            
            if x.takable:
                if x.set_location([self]):
                    print(used_verb)
                    continue
                print("You can't carry more stuff right now.")

            else:
                print("That isn't really feasible, I'm afraid.")
    
    def drop(self, direct, indirect, used_verb):

        if not indirect:
            indirect = self.location[0]
        
        for x in direct:
            if len(direct) > 1:
                print('(' + x.name + ')', end=' ')
        
            if not x in self.contents:
                print("You aren't holding that!")
                continue

            if x.set_location([indirect]):
                print(used_verb)
                continue

            print("There's no room in the " + indirect.name + ".")
    
    def look(self, direct, indirect, used_verb):

        if not direct:
            direct = self.location
        
        direct = direct[0]
        
        if not self.can_touch(direct):
            print("You don't see any " + direct.name + " here!")
            return
        
        print(direct.describe())
    
    def inventory(self, direct, indirect, used_verb):
        ans = []
        for x in self.contents:
            if x.displayable:
                ans.append(x)
        
        if not ans:
            print("You are empty handed.")
            return
        
        ans = self.formatted_contents()

        ans = "You are holding:\n" + ans

        print(ans)
    
    def has_item_in_inventory(self, item):
        return super().find_object_by_name(item)
    
    def can_touch(self, item):
        room = self.location

        ans = [item]
        new_ans = []

        while True:
            for x in ans:
                if type(x) is Room:
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

        
