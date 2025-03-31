import nltk
from nltk.corpus import wordnet

# Download WordNet if not already available
nltk.download("wordnet")

class GrammarRules:
    def __init__(self):
        self.articles = {"the", "a", "an"}  # Fixed articles

    def is_noun(self, word):
        """Check if a word is a noun using WordNet."""
        synsets = wordnet.synsets(word)
        return any(syn.pos() == "n" for syn in synsets)

    def is_verb(self, word):
        """Check if a word is a verb using WordNet."""
        synsets = wordnet.synsets(word)
        return any(syn.pos() == "v" for syn in synsets)
