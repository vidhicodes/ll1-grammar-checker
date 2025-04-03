import streamlit as st
from parser_logic import compute_first_follow, construct_ll1_table, parse_sentence
from agreement import validate_sentence

st.set_page_config(layout="wide")

# UI Title
st.title("Grammar Checker & LL(1) Parser")

# Sentence Input
sentence = st.text_input("Enter a sentence:", "")

# Buttons Layout
col1, col2, col3, col4, col5 = st.columns(5)

if col1.button("Check Sentence"):
    if sentence:
        result, steps = parse_sentence(sentence)
        if result:
            st.success("✅ Valid Sentence")
        else:
            st.error("❌ Invalid Sentence")
        if steps:
            st.subheader("Parsing Steps")
            st.table(steps)
    else:
        st.error("Please enter a sentence.")

if col2.button("Compute FIRST & FOLLOW"):
    first_sets, follow_sets = compute_first_follow()
    st.subheader("FIRST Sets")
    st.json(first_sets)
    st.subheader("FOLLOW Sets")
    st.json(follow_sets)

if col3.button("Display Parsing Table"):
    parsing_table = construct_ll1_table()
    st.subheader("LL(1) Parsing Table")
    st.json(parsing_table)

if col4.button("Validate Sentence Structure"):
    if sentence:
        is_valid = validate_sentence(sentence)
        if is_valid:
            st.success("✅ Sentence format is valid.")
        else:
            st.error("❌ Invalid Sentence Format")
    else:
        st.error("Please enter a sentence.")

if col5.button("Exit"):
    st.stop()
