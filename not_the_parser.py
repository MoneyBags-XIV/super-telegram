class Parser:
    def __init__(self, player, game):
        self.game = game
        self.player = player
    
    def parse(self, str):

        verb = ''
        direct = ''
        indirect = ''

        if not str:
            print("Pardon?")
            return verb, direct, indirect
        

        str = str.split(' ')

        verb = str[0]
        verb = getattr(self.player, verb)

        if len(str) > 1:
            direct = str[1]
            direct = self.game.find_object_by_name(direct)
        
        if len(str) > 2:
            indirect = str[2]
            indirect = self.game.find_object_by_name(indirect)
        
        return verb, direct, indirect
