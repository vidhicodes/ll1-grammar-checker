import streamlit as st
from parser import parse_sentence
from first_follow import compute_first_follow
from parsing_table import construct_ll1_table

st.title("LL(1) Grammar Checker & Parser")

sentence = st.text_input("Enter a sentence:")

if st.button("Check Sentence"):
    is_valid, steps = parse_sentence(sentence)
    if is_valid:
        st.success("✅ The sentence is valid!")
    else:
        st.error("❌ Invalid sentence. Check parsing steps.")

if st.button("Show Parsing Steps"):
    if sentence:
        _, steps = parse_sentence(sentence)
        st.write("### Parsing Steps")
        for step in steps:
            st.write(step)

if st.button("Show FIRST & FOLLOW Sets"):
    first, follow = compute_first_follow()
    st.write("### FIRST Sets")
    st.write(first)
    st.write("### FOLLOW Sets")
    st.write(follow)

if st.button("Show Parsing Table"):
    table = construct_ll1_table()
    st.write("### LL(1) Parsing Table")
    st.write(table)
