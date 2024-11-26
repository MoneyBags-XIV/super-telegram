class Parser:
    def __init__(self, verbosity):
        self.verbosity = verbosity
    
    def parse(self, str):

        if not str:
            print("Pardon?")
            return