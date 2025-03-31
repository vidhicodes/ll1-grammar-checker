from parser import LL1Parser

if __name__ == "__main__":
    parser = LL1Parser()

    while True:
        sentence = input("\nEnter a sentence (or type 'exit' to quit): ").strip().lower()
        if sentence == "exit":
            break

        tokens = sentence.split()
        tokens.append("$")  # End-of-input marker

        if parser.parse(tokens):
            print("✅ Valid Sentence!")
        else:
            print("❌ Invalid Sentence!")
