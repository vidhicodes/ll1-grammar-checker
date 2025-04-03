import streamlit as st
import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from tabulate import tabulate  

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()

# Grammar Rules
grammar_rules = {
    "S": ["NP VP"],
    "NP": ["Det N", "N", "PRP"],
    "VP": ["V", "V NP", "V PP"],
    "PP": ["P NP"],
}

start_symbol = "S"
first, follow = {}, {}

# Compute FIRST sets
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

# Compute FOLLOW sets
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

# Construct LL(1) Parsing Table
def construct_ll1_table():
    table = {}
    for nt, rules in grammar_rules.items():
        for rule in rules:
            first_set = set()
            rule_symbols = rule.split()
            for s in rule_symbols:
                first_set |= get_first(s)
                if "ε" not in get_first(s):
                    break
            else:
                first_set |= get_follow(nt)
            
            for terminal in first_set - {"ε"}:
                table[(nt, terminal)] = rule

            if "ε" in first_set:
                for terminal in follow[nt]:
                    table[(nt, terminal)] = rule
    return table

# Compute FIRST, FOLLOW, and Parsing Table
for nt in grammar_rules:
    get_first(nt)
    get_follow(nt)

ll1_table = construct_ll1_table()

# Subject-Verb Agreement Functions
def is_singular_verb(verb):
    base_form = lemmatizer.lemmatize(verb, 'v')
    return verb != base_form

def check_subject_verb_agreement(subject, subject_tag, verb):
    verb_is_singular = is_singular_verb(verb)
    singular_subjects = ["he", "she", "it"]
    plural_subjects = ["they", "we", "you"]

    if subject in singular_subjects and not verb_is_singular:
        return False
    if subject in plural_subjects and verb_is_singular:
        return False
    if subject_tag in ["NN", "DT NN"] and not verb_is_singular:
        return False
    if subject_tag in ["NNS", "DT NNS"] and verb_is_singular:
        return False
    return True

# Sentence Parsing with Steps
def parse_sentence(sentence):
    if not sentence[0].isupper() or sentence[-1] not in ".!?":
        return "Invalid Sentence: Incorrect format.", []

    words = word_tokenize(sentence[:-1].lower()) + ["$"]
    tagged_words = pos_tag(words)

    stack = ["$", start_symbol]
    pointer = 0
    subject = None
    subject_tag = None
    parsing_steps = []
    step = 1

    while stack:
        top = stack[-1]
        remaining_input = " ".join(words[pointer:])

        if top == words[pointer]:
            action = f"Matched '{top}', consuming input"
            stack.pop()
            pointer += 1
        elif top in grammar_rules:
            stack.pop()
            rule = ll1_table.get((top, words[pointer]), None)
            if rule:
                stack.extend(reversed(rule.split()))
                action = f"Expanding {top} → {rule}"
            else:
                return "Invalid Sentence: Parsing failed.", []
        elif top in ["N", "PRP", "Det"]:
            word, tag = tagged_words[pointer]
            if top == "N" and tag in ["NN", "NNS"]:
                stack.pop()
                subject, subject_tag = word, tag
                pointer += 1
                action = f"Matched Noun '{word}'"
            elif top == "PRP" and tag.startswith("PRP"):
                stack.pop()
                subject, subject_tag = word, tag
                pointer += 1
                action = f"Matched Pronoun '{word}'"
            elif top == "Det" and tag == "DT":
                stack.pop()
                pointer += 1
                action = f"Matched Determiner '{word}'"
            else:
                return "Invalid Sentence: Incorrect subject form.", []
        elif top == "V":
            word, tag = tagged_words[pointer]
            if tag.startswith("VB"):
                stack.pop()
                if subject and not check_subject_verb_agreement(subject, subject_tag, word):
                    return f"Invalid: Subject-Verb Agreement Failed ('{subject}' → '{word}').", []
                pointer += 1
                action = f"Matched Verb '{word}'"
            else:
                return "Invalid: Missing or incorrect verb.", []
        else:
            return "Invalid: Parsing failed.", []

        parsing_steps.append((step, " ".join(stack), remaining_input, action))
        step += 1

    return "✅ Valid Sentence" if pointer == len(words) else "❌ Invalid Sentence", parsing_steps

# Streamlit UI
st.title("Grammar Checker & LL(1) Parser")

sentence = st.text_input("Enter a sentence:", "")

if st.button("Check Sentence"):
    result, steps = parse_sentence(sentence)
    st.write(result)

if st.button("Display First Sets"):
    st.text(tabulate([(k, ', '.join(v)) for k, v in first.items()], headers=["Non-Terminal", "FIRST"], tablefmt="grid"))

if st.button("Display Follow Sets"):
    st.text(tabulate([(k, ', '.join(v)) for k, v in follow.items()], headers=["Non-Terminal", "FOLLOW"], tablefmt="grid"))

if st.button("Display Parsing Table"):
    headers = ["Non-Terminal"] + sorted({t for (_, t) in ll1_table.keys()}) + ["$"]
    rows = [[nt] + [ll1_table.get((nt, terminal), "∅") for terminal in headers[1:]] for nt in grammar_rules]
    st.text(tabulate(rows, headers, tablefmt="grid"))

if st.button("Show Parsing Steps"):
    _, steps = parse_sentence(sentence)
    if steps:
        st.table(steps)
    else:
        st.write("No parsing steps available.")
