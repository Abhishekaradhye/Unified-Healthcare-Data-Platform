import streamlit as st
import requests

st.title("Unified Data Search (Multiple Queries)")

contexts_input = st.text_area(
    "Enter one or more transaction_ids or patient_ids (one per line):",
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
        for item in results:
            for key, val in item.items():
                st.subheader(f"Query: {key}")
                st.json(val)
    else:
        st.error("Failed to fetch data")


# streamlit run self_frontend.py

# FRONTEND FOR 'self_finance_api' , 'self_staff_api' , 'self_patients_api' FILES

# SUCCESSFULLY FETCHED SELF AWARE API CALLS