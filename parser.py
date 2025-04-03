import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from first_follow import grammar_rules

def parse_sentence(sentence):
    if not sentence:
        return False, []

    sentence = sentence[:-1].lower() + " $"
    words = word_tokenize(sentence)
    tagged_words = pos_tag(words)

    stack = ["$", "S"]
    pointer = 0
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
            stack.extend(reversed(grammar_rules[top][0].split()))
            action = f"Expanding {top} → {grammar_rules[top][0]}"
        else:
            return False, []

        parsing_steps.append((step, " ".join(stack), remaining_input, action))
        step += 1

    return pointer == len(words), parsing_steps
