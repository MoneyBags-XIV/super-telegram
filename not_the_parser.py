class Parser:
    def __init__(self, player, game, verb_list):
        self.game = game
        self.player = player
        self.verb_list = verb_list
    
    def parse(self):

        while True:
            input_str = input("> ")

            if not input_str:
                print("Pardon?")
                continue

            input_str= input_str.lower()
            clean_chars = ['.', ',', '\'']
            for x in clean_chars:
                input_str= input_str.replace(x, '')
            words = input_str.split(" ")

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
                            used_verb = ans
                        
            if not verbs:
                print("There's no verb in that sentence!")
                continue

            if len(verbs) > 1:
                print("There are too many verbs in that sentence!")
                continue

            verb = verbs[0]

            output = verb.parse_nouns(words, used_verb)

            if type(output) is str:
                print(output)
                continue

            return output


class Verb:
    def __init__(self, verbs, player, expects_direct=False, needs_direct=False, accepts_multiple_direct=False, needs_indirect=False):
        self.verbs = verbs

        self.expects_direct = expects_direct
        self.needs_direct = needs_direct
        self.accepts_multiple_direct = accepts_multiple_direct

        self.needs_indirect = needs_indirect

        self.player_method = getattr(player, self.verbs[0])
        self.game = player.game
    
    def parse_nouns(self, words, used_verb):

        direct = None
        indirect = None

        if not self.expects_direct:
            return (self.player_method, direct, indirect)
        
        indirect, words = self.get_indirect(words)

        if indirect and not self.needs_indirect:
            return "That sentence doesn't make sense."
        
        direct = self.get_direct(words)

        if not direct and self.needs_direct:
            ans = input("What do you want to " + used_verb + "?\n> ")
            direct = self.find_nouns(ans)
            if not direct:
                return "I don't understand what you want to do."
        
        if len(direct) > 1 and not self.accepts_multiple_direct:
            return "You can't use multiple direct objects with the verb: \"" + used_verb + ".\""
        
        if not self.needs_indirect:
            return (self.player_method, direct, indirect)
        
        if not indirect:
            ans = input("What do you want to " + used_verb + " the " + direct + " with?\n> ")
            indirect = self.find_nouns(ans)
            if not indirect:
                return "Good luck with that!"
        
        if len(indirect) > 1:
            return "You can't do that."
        
        return (self.player_method, direct, indirect)

        

    def get_direct(self, words):
        return self.find_nouns(' '.join(words))

    def get_indirect(self, words):

        og_words = words
        
        clean_words = ["a", "the", "your", "my"]
        
        words = [x for x in words if x not in clean_words]

        que_word = None
        for word in words:
            if word in ["use", "using", "with"]:
                if que_word:
                    return (None, og_words)
                que_word = word
                
        if not que_word:
            return (None, og_words)
        
        start_index = words.index(que_word) + 1
        words = words[start_index:]

        nouns = []

        for i in range(len(words)):
            ans = words[:i+1]
            object = self.game.find_object_by_name(' '.join(ans))
            if object:
                if not object in nouns:
                    nouns.append(object)
                    name = ' '.join(ans)
                
        if len(nouns) > 1 or not nouns:
            return (None, og_words)
        
        og_words.reverse()
        og_words.remove(name)
        og_words.reverse()
        
        return (nouns[0], og_words)


    def find_nouns(self, thing):
        thing = thing.lower()
        clean_chars = ['.', ',', '\'']
        for x in clean_chars:
            thing = thing.replace(x, '')
        words = thing.split(" ")

        nouns = []

        for i in range(len(words)):
            for j in range(i+1):
                ans = words[j:j+len(words)-i]
                ans = " ".join(ans)

                x = self.game.find_object_by_name(ans)

                if x:
                    nouns.append(x)
                        
        return nouns