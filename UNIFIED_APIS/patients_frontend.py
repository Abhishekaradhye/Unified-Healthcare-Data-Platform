import streamlit as st
import requests

st.title("Unified Patients Data Search")

st.write("Enter each new query on a new line to fetch the top result:")

context_list = st.text_area("Enter queries, one per line").split("\n")

if st.button("Search"):
    for context in context_list:
        if context.strip() == "":
            continue
        response = requests.post(
            "http://127.0.0.1:8000/search",
            json={"context": context.strip()}
        )
        if response.status_code == 200:
            result = response.json()
            st.write(f"Query: {context.strip()}")
            st.json(result)
        else:
            st.error(f"Failed to fetch data for: {context.strip()}")


# streamlit run patients_frontend.py

# FRONTEND FOR 'PATIENTS_FETCHED' FILE IN 'UNIFIED_APIS' DIRECTORY, WHICH WAS A RAG BASED SEARCH.