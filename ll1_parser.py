import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import tkinter as tk
from tkinter import messagebox, ttk
from collections import defaultdict
from tabulate import tabulate  

lemmatizer = WordNetLemmatizer()

grammar_rules = {
    "S": ["NP VP"],
    "NP": ["Det N", "N", "PRP"],
    "VP": ["V", "V NP", "V PP"],
    "PP": ["P NP"],
}

start_symbol = "S"

first, follow = {}, {}

def get_first(symbol):
    """Compute FIRST sets"""
    if symbol in first:
        return first[symbol]

    first[symbol] = set()
    
    # If symbol is a terminal, return itself
    if symbol not in grammar_rules:  
        first[symbol].add(symbol)
        return first[symbol]

    # Process non-terminals
    for rule in grammar_rules[symbol]:
        rule_symbols = rule.split()  # Split rule into symbols
        for s in rule_symbols:
            f = get_first(s)
            first[symbol] |= (f - {"ε"})  # Add FIRST(s) except ε
            if "ε" not in f:
                break
        else:
            first[symbol].add("ε")  # If all symbols have ε, add ε
    
    return first[symbol]



def get_follow(non_term):
    """Compute FOLLOW sets"""
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


def construct_ll1_table():
    """Build LL(1) Parsing Table"""
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


# Compute FIRST and FOLLOW sets
for nt in grammar_rules:
    get_first(nt)
    get_follow(nt)

# Construct LL(1) Parsing Table
ll1_table = construct_ll1_table()

# Get sorted list of terminals
terminals = sorted({t for (_, t) in ll1_table.keys()})
terminals.append('$')

def print_table():
    """Print LL(1) Parsing Table"""
    headers = ["Non-Terminal"] + terminals
    rows = []
    
    for nt in grammar_rules:
        row = [nt]
        for terminal in terminals:
            rule = ll1_table.get((nt, terminal), [])
            row.append(f"{nt} → {rule}" if rule else "∅")
        rows.append(row)

    print(tabulate(rows, headers))

# Print Results
print("\n FIRST Sets:", first)
print("\n FOLLOW Sets:", follow)
print("\n LL(1) Parsing Table:")
print_table()
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

def validate_sentence(sentence):
    if not sentence[0].isupper():
        messagebox.showerror("Grammar Check", "Invalid: Sentence must start with a capital letter.")
        return False
    if sentence[-1] not in ".!?":
        messagebox.showerror("Grammar Check", "Invalid: Sentence must end with '.', '!', or '?'")
        return False
    words = sentence[:-1].split()
    if len(words) < 2:
        messagebox.showerror("Grammar Check", "Invalid: Sentence too short.")
        return False
    return True

def parse_sentence(sentence):
    if not validate_sentence(sentence):
        return False
    
    sentence = sentence[:-1].lower() + " $"
    words = word_tokenize(sentence)
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
            if top == "S":
                stack.extend(reversed(["NP", "VP"]))
                action = "Expanding S → NP VP"
            elif top == "NP":
                if tagged_words[pointer][1] == "PRP":
                    stack.append("PRP")
                    action = "Expanding NP → PRP"
                elif tagged_words[pointer][1] in ["DT", "NN", "NNS"]:
                    stack.extend(reversed(["N"]))
                    if tagged_words[pointer][1] == "DT":
                        stack.append("Det")
                    action = "Expanding NP → Det N" if tagged_words[pointer][1] == "DT" else "Expanding NP → N"
            elif top == "VP":
                if pointer + 1 < len(words) and tagged_words[pointer + 1][1] in ["DT", "NN", "NNS"]:
                    stack.extend(reversed(["V", "NP"]))
                    action = "Expanding VP → V NP"
                else:
                    stack.append("V")
                    action = "Expanding VP → V"
        
        elif top in ["N", "PRP", "Det"]:
            word, tag = tagged_words[pointer]
            if top == "N" and tag in ["NN", "NNS"]:
                stack.pop()
                subject = word
                subject_tag = tag
                pointer += 1
                action = f"Matched Noun '{word}'"
            elif top == "PRP" and tag.startswith("PRP"):
                stack.pop()
                subject = word
                subject_tag = tag
                pointer += 1
                action = f"Matched Pronoun '{word}'"
            elif top == "Det" and tag == "DT":
                stack.pop()
                pointer += 1
                action = f"Matched Determiner '{word}'"
            else:
                messagebox.showerror("Grammar Check", "Invalid Sentence: Incorrect subject form.")
                return False
        
        elif top == "V":
            word, tag = tagged_words[pointer]
            if tag.startswith("VB"):
                stack.pop()
                if subject and not check_subject_verb_agreement(subject, subject_tag, word):
                    messagebox.showerror("Grammar Check", f"Invalid: Subject-Verb Agreement Failed ('{subject}' → '{word}').")
                    return False
                pointer += 1
                action = f"Matched Verb '{word}'"
            else:
                messagebox.showerror("Grammar Check", "Invalid: Missing or incorrect verb.")
                return False
        else:
            messagebox.showerror("Grammar Check", "Invalid: Parsing failed.")
            return False

        parsing_steps.append((step, " ".join(stack), remaining_input, action))
        step += 1
    
    update_parsing_table(parsing_steps)
    
    if pointer == len(words):
        messagebox.showinfo("Grammar Check", "✅ Valid Sentence")
        return True
    else:
        messagebox.showerror("Grammar Check", "❌ Invalid Sentence")
        return False

def update_parsing_table(parsing_steps):
    tree.delete(*tree.get_children())
    for step in parsing_steps:
        tree.insert("", "end", values=step)

def check_sentence():
    sentence = entry.get().strip()
    if sentence:
        parse_sentence(sentence)
    else:
        messagebox.showerror("Input Error", "Please enter a sentence.")

root = tk.Tk()
root.title("Grammar Checker")
root.geometry("600x400")

label = tk.Label(root, text="Enter a sentence:", font=("Arial", 12))
label.pack(pady=5)

entry = tk.Entry(root, width=50, font=("Arial", 12))
entry.pack()

button = tk.Button(root, text="Check", command=check_sentence, font=("Arial", 12), bg="blue", fg="white")
button.pack(pady=5)

table_label = tk.Label(root, text="Parsing Steps:", font=("Arial", 12, "bold"))
table_label.pack(pady=5)

columns = ("Step", "Stack", "Remaining Input", "Action")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)
tree.pack(fill="both", expand=True, padx=10, pady=5)

root.mainloop()
