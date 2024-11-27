class Parser:
    def __init__(self, game):
        self.game = game
    
    def parse(self, str):

        if not str:
            print("Pardon?")
            return
        
        return