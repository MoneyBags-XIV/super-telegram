class Parser:
    def __init__(self, player, game, verb_list):
        self.game = game
        self.player = player
        self.verb_list = verb_list
    
    def parse(self):

        while True:
            str = input("> ")
            str = str.lower()
            clean_chars = ['.', ',', '\'']
            for x in clean_chars:
                str = str.replace(x, '')
            words = str.split(" ")

            verbs = []

            #TODO find multiple objects with the same name and default to one in same room, or ask which one

            # this is just to check all combinations of consecutive words for multi-word verbs (I am proud of it)
            for i in range(len(words)):
                for j in range(i+1):
                    ans = words[j:j+len(words)-i]
                    ans = " ".join(ans)
                    for x in self.verb_list:
                        if ans in x.verbs and not x in verbs:
                            verbs.append(x)
                        
            if not verbs:
                print("There's no verb in that sentence!")
                continue

            if len(verbs) > 1:
                print("There are too many verbs in that sentence!")
                continue

            verb = verbs[0]

            output = verb.parse_nouns(words)


class Verb:
    def __init__(self, verbs, player, expects_direct=False, needs_direct=False, accepts_multiple_direct=False, expects_indirect=False, needs_indirect=False):
        self.verbs = verbs

        self.expects_direct = expects_direct
        self.needs_direct = needs_direct
        self.accepts_multiple_direct = accepts_multiple_direct

        self.expects_indirect = expects_indirect
        self.needs_indirect = needs_indirect

        self.player_method = getattr(player, self.verbs[0])
        self.game = self.player.game
    
    def parse_nouns(self, words):

        direct = None
        indirect = None

        if not self.expects_direct:
            return direct, indirect
        
        indirect = self.get_indirect(words)

        if indirect and not self.expects_indirect:
            return "That sentence doesn't make sense."
        
        

    def get_direct(self, words):
        pass

    def get_indirect(self, words):
        pass

    def find_nouns(self, words):
        nouns = []

        for i in range(len(words)):
            for j in range(i+1):
                ans = words[j:j+len(words)-i]
                ans = " ".join(ans)

                x = self.game.find_object_by_name(ans)

                if x:
                    nouns.append(x)