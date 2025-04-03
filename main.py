import streamlit as st
from first_follow import compute_first_follow
from parsing_table import construct_ll1_table
from parser import parse_sentence
from sentence_validator import validate_sentence
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')  # Required for POS tagging

# Compute FIRST & FOLLOW sets
first, follow = compute_first_follow()

# Compute LL(1) Parsing Table
parsing_table = construct_ll1_table()

st.set_page_config(layout="wide")

st.title("LL(1) Grammar Checker & Parser")

sentence = st.text_input("Enter a sentence:")

if st.button("Check Sentence"):
    if validate_sentence(sentence):
        is_valid, steps = parse_sentence(sentence)
        if is_valid:
            st.success("✅ Valid Sentence")
            st.subheader("Parsing Steps")
            st.table(steps)
        else:
            st.error("❌ Invalid Sentence")

if st.button("Show FIRST Sets"):
    st.subheader("FIRST Sets")
    st.table([(nt, ', '.join(v)) for nt, v in first.items()])

if st.button("Show FOLLOW Sets"):
    st.subheader("FOLLOW Sets")
    st.table([(nt, ', '.join(v)) for nt, v in follow.items()])

if st.button("Show Parsing Table"):
    st.subheader("LL(1) Parsing Table")
    table_headers = ["Non-Terminal"] + sorted(set(t for (_, t) in parsing_table.keys())) + ["$"]
    table_rows = [[nt] + [parsing_table.get((nt, terminal), "∅") for terminal in table_headers[1:]] for nt in first.keys()]
    st.table(table_rows)
