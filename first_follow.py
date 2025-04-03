from collections import defaultdict

# Grammar Rules
grammar_rules = {
    "S": ["NP VP"],
    "NP": ["Det N", "N", "PRP"],
    "VP": ["V", "V NP", "V PP"],
    "PP": ["P NP"],
}

start_symbol = "S"
first, follow = {}, {}

def get_first(symbol):
    if symbol in first:
        return first[symbol]

    first[symbol] = set()
    if symbol not in grammar_rules:
        first[symbol].add(symbol)
        return first[symbol]

    for rule in grammar_rules[symbol]:
        rule_symbols = rule.split()
        for s in rule_symbols:
            f = get_first(s)
            first[symbol] |= (f - {"ε"})
            if "ε" not in f:
                break
        else:
            first[symbol].add("ε")

    return first[symbol]

def get_follow(non_term):
    if non_term in follow:
        return follow[non_term]

    follow[non_term] = set()
    if non_term == start_symbol:
        follow[non_term].add("$")

    for lhs, rules in grammar_rules.items():
        for rule in rules:
            rule_symbols = rule.split()
            for i, symbol in enumerate(rule_symbols):
                if symbol == non_term:
                    next_part = rule_symbols[i+1:]
                    if next_part:
                        first_next = set()
                        for s in next_part:
                            first_next |= get_first(s)
                            if "ε" not in get_first(s):
                                break
                        else:
                            follow[non_term] |= get_follow(lhs)
                        follow[non_term] |= (first_next - {"ε"})
                    else:
                        follow[non_term] |= get_follow(lhs)

    return follow[non_term]

def compute_first_follow():
    for nt in grammar_rules:
        get_first(nt)
        get_follow(nt)
    return first, follow
