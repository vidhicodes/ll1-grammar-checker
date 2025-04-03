from agreement import validate_sentence

def simple_tokenize(sentence):
    return sentence.split()

def parse_sentence(sentence):
    sentence = sentence.strip()
    if not validate_sentence(sentence):
        return False, []

    words = simple_tokenize(sentence)

    stack = ["$", "S"]
    pointer = 0
    parsing_steps = []

    while stack:
        top = stack.pop()
        remaining_input = " ".join(words[pointer:])

        if pointer < len(words) and top == words[pointer]:
            action = f"Matched '{top}', consuming input"
            pointer += 1
        elif top in ["NP", "VP", "N", "V"]:
            stack.extend(reversed(["N", "V"]))
            action = f"Expanding {top} → N V"
        else:
            return False, parsing_steps

        parsing_steps.append((top, remaining_input, action))

    return pointer == len(words), parsing_steps
