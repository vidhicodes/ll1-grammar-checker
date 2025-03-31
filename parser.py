from grammar import GrammarRules

class LL1Parser:
    def __init__(self):
        self.grammar = {
            "S": [["NP", "VP"]],
            "NP": [["ART", "NOUN"]],
            "VP": [["VERB", "NP"], ["VERB"]],
        }
        self.grammar_rules = GrammarRules()
        self.stack = []

    def parse(self, tokens):
        """LL(1) Parsing Implementation using Stack"""
        self.stack = ["$", "S"]  # Start symbol
        index = 0

        while len(self.stack) > 0:
            top = self.stack.pop()
            if top == tokens[index]:  # Terminal match
                index += 1
            elif top == "ART" and tokens[index] in self.grammar_rules.articles:
                index += 1
            elif top == "NOUN" and self.grammar_rules.is_noun(tokens[index]):
                index += 1
            elif top == "VERB" and self.grammar_rules.is_verb(tokens[index]):
                index += 1
            elif top in self.grammar:  # Non-terminal expansion
                rule_found = False
                for production in self.grammar[top]:
                    if production[0] in ["ART", "NOUN", "VERB"] or production[0] == tokens[index]:
                        self.stack.extend(reversed(production))
                        rule_found = True
                        break
                if not rule_found:
                    return False
            else:
                return False

        return index == len(tokens)
