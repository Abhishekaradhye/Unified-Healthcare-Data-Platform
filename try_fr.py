import streamlit as st
import requests
import json

st.title("Patient Data Search (Multiple Queries)")

contexts_input = st.text_area(
    "Enter one or more queries (each line is a query):",
    height=150
)

if st.button("Search"):
    contexts = [line.strip() for line in contexts_input.split("\n") if line.strip()]
    response = requests.post(
        "http://127.0.0.1:8000/search_multiple",
        json={"contexts": contexts}
    )
    if response.status_code == 200:
        results = response.json()
        st.json(results)  # displays each context with corresponding top_k matches
    else:
        st.error("Failed to fetch data")


# streamlit run try_fr.py
# FRONTEND FOR TRY5 & TRY6 