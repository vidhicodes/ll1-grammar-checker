from grammar import GrammarRules

class LL1Parser:
    def __init__(self):
        self.grammar = GrammarRules()
        self.tokens = []
        self.current_token_index = 0
    
    def parse(self, sentence):
        self.tokens = sentence.lower().split()
        self.tokens.append("$")  # End of input marker
        self.current_token_index = 0
        return self.sentence() and self.match("$")

    def match(self, expected):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index] == expected:
            self.current_token_index += 1
            return True
        return False

    def match_any(self, token_list):
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index] in token_list:
            self.current_token_index += 1
            return True
        return False

    def sentence(self):
        return self.noun_phrase() and self.verb_phrase()

    def noun_phrase(self):
        return self.match_any(self.grammar.articles) and self.match_any(self.grammar.nouns)

    def verb_phrase(self):
        return self.match_any(self.grammar.verbs) and self.match_any(self.grammar.objects)

