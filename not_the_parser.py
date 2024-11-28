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

            for i in range(len(words)):
                for j in range(i+1):
                    ans = words[j:len(words)-i]
                    ans = " ".join(ans)
                    for x in self.verb_list:
                        if ans in x.verbs:
                            verbs.append(x)
            
            #TODO check for duplicates
            
            if not verbs:
                print("There's no verb in that sentance!")
                continue

            if len(verbs) > 1:
                print("There are too many verbs in that sentance!")
                continue

            verb = verbs[0]

            #TODO allow verbs to take direct object, but not need one
    
            if not verb.expects_direct:
                return verb.player_method, None, None
            
            nouns = []
            
            for i in range(len(words)):
                for j in range(i+1):
                    ans = words[j:len(words)-i]
                    ans = " ".join(ans)
                    if self.game.find_object_by_name(ans):
                        nouns.append(ans)
            
            # if not self.accepts_multiple_direct and len(nouns) > 1:


class Verb:
    def __init__(self, verbs, player, expects_direct=False, expects_indirect=False, accepts_multiple_direct=False):
        self.verbs = verbs
        self.expects_direct = expects_direct
        self.expects_indirect = expects_indirect
        self.player_method = getattr(player, self.verbs[0])
        self.accepts_multiple_direct = accepts_multiple_direct
    
    # def find_direct(self, words, game):
    #     if not self.expects_direct:
    #         return
        
    #     nouns = []
        
    #     for i in range(len(words)):
    #         for j in i+1:
    #             ans = words[j:len(words)-i]
    #             ans = " ".join(ans)
    #             if game.find_object_by_name(ans):
    #                 nouns.append(ans)
        
    #     if not self.accepts_multiple_direct and len(nouns) > 1:
            
                
        

