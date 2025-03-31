from tkinter import *
from parser import LL1Parser

class GrammarCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("LL(1) Parser - Grammar Checker")
        self.root.geometry("500x250")

        Label(root, text="Enter a Sentence:", font=("Arial", 12)).pack(pady=10)
        self.entry = Entry(root, width=50, font=("Arial", 12))
        self.entry.pack()

        self.result_label = Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)

        Button(root, text="Check Grammar", command=self.check_grammar, font=("Arial", 12)).pack()

    def check_grammar(self):
        sentence = self.entry.get().strip().lower().split()
        sentence.append("$")  # End-of-input marker

        parser = LL1Parser()
        if parser.parse(sentence):
            self.result_label.config(text="Valid Sentence ✔️", fg="green")
        else:
            self.result_label.config(text="Invalid Sentence ❌", fg="red")

if __name__ == "__main__":
    root = Tk()
    GrammarCheckerGUI(root)
    root.mainloop()

