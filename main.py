from tkinter import *
from parser import LL1Parser

class GrammarCheckerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("English Grammar Checker (LL(1) Parser)")
        
        Label(root, text="Enter an English Sentence:", font=("Arial", 12)).pack(pady=10)
        
        self.text_entry = Entry(root, width=50, font=("Arial", 12))
        self.text_entry.pack(pady=5)
        
        self.result_label = Label(root, text="", font=("Arial", 12), fg="blue")
        self.result_label.pack(pady=10)
        
        Button(root, text="Check Grammar", font=("Arial", 12), command=self.check_grammar).pack(pady=5)
    
    def check_grammar(self):
        sentence = self.text_entry.get().strip()
        parser = LL1Parser()
        if parser.parse(sentence):
            self.result_label.config(text="Valid Sentence ✔️", fg="green")
        else:
            self.result_label.config(text="Invalid Sentence ❌", fg="red")

if __name__ == "__main__":
    root = Tk()
    gui = GrammarCheckerGUI(root)
    root.mainloop()
