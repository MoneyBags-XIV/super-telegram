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

            words = clean_input(input_str)

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
    def __init__(self, verbs, player, past_participles=None, expects_direct=False, needs_direct=False, accepts_multiple_direct=False, expects_indirect=False, needs_indirect=False):
        self.verbs = verbs
        self.past_participles = past_participles if past_participles else verbs

        self.expects_direct = expects_direct
        self.needs_direct = needs_direct
        self.accepts_multiple_direct = accepts_multiple_direct

        self.expects_indirect = expects_indirect
        self.needs_indirect = needs_indirect

        self.player_method = getattr(player, self.verbs[0])
        self.player = player
        self.game = player.game

        self.had_to_ask = False
    
    def parse_nouns(self, words, used_verb):

        direct = None
        indirect = None

        participle = self.past_participles[self.verbs.index(used_verb)]

        if not self.expects_direct:
            return (self.player_method, direct, indirect, participle)

        if self.expects_indirect:
            indirect, words = self.get_indirect(words)
        
        direct = self.get_direct(words, used_verb=used_verb)

        if not direct and self.needs_direct:
            return "I don't understand what you want to do."
        
        if len(direct) > 1 and not self.accepts_multiple_direct:
            return "You can't use multiple direct objects with the verb: \"" + used_verb + ".\""
        
        if not self.expects_indirect:
            return (self.player_method, direct, indirect, participle)
        
        if not indirect and self.needs_indirect:
            ans = input("What do you want to " + used_verb + " the " + direct + " with?\n> ")
            ans = clean_input(ans)
            indirect = self.find_nouns(ans)
            if not indirect:
                return "Good luck with that!"
        
            if len(indirect) > 1:
                return "You can't do that."
        
        return (self.player_method, direct, indirect, participle)

        

    def get_direct(self, words, used_verb):
        nouns = self.find_nouns(' '.join(words))
        nouns = set(nouns)
        nouns = list(nouns)

        if self.had_to_ask:
            self.had_to_ask = False # I know this is awkward
            return nouns

        if not nouns and self.needs_direct:
            ans = input("What do you want to " + used_verb + "?\n> ")
            ans = clean_input(ans)
            nouns = self.find_nouns(' '.join(ans))
            nouns = set(nouns)
            nouns = list(nouns)
        
        self.had_to_ask = False
        return nouns

    def get_indirect(self, words):

        og_words = words
        
        clean_words = ["a", "the", "your", "my"]
        
        words = [x for x in words if x not in clean_words]

        que_word = None
        for word in words:
            if word in ["use", "using", "with", "in", "inside", "into", "at", "to"]:
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
                ans = words[i:i+len(words)-j]
                ans = " ".join(ans)

                x = self.game.find_object_by_name(ans)

                if x:
                    if len(x) > 1:
                        nouns += self.clarify_noun(x, ans)
                        self.had_to_ask = True
                        
                
                    else:
                        nouns.append(x[0])
                    
                    new_words = words[:i] + words[i+len(words)-j:]
                    new_words = ' '.join(new_words)
                    nouns += self.find_nouns(new_words)
                    return nouns

        return nouns
    
    def clarify_noun(self, x, unclear_word):
        
        # This code was really annoying to write. I couldn't think of a good way to do it. No judgement please.
        x = [y for y in x if self.player.can_touch(y)]

        if len(x) > 1:
            string = "Which " + unclear_word + " do you mean? The " + x[0].name + ', '
            for k in range(1, len(x)-1):
                string += 'the ' + k.name + ', '
            string += "or the " + x[-1].name + '?\n> '

            asdf = input(string)
            asdf = clean_input(asdf)
            if 'all' in asdf or 'both' in asdf:
                return x
            
            for word in asdf:
                for item in x:
                    for synonym in item.synonyms:
                        a = clean_input(synonym)
                        a = [b for b in a if b != unclear_word]
                        if word in a:
                            return [item]
            
            return []

def clean_input(string):

    input_str= string.lower()
    clean_chars = ['.', ',', '\'']
    for x in clean_chars:
        input_str= input_str.replace(x, '')
    words = input_str.split(" ")

    return words