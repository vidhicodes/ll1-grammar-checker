from nltk.stem import WordNetLemmatizer
import nltk

nltk.download("wordnet")
lemmatizer = WordNetLemmatizer()

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
        return False
    if sentence[-1] not in ".!?":
        return False
    words = sentence[:-1].split()
    if len(words) < 2:
        return False
    return True
