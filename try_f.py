import streamlit as st
import requests

st.title("HIS_A Patients Self-Aware API")

ids_input = st.text_input("Enter patient IDs (comma-separated):", "4,10,14")

if st.button("Fetch Data"):
    url = f"http://127.0.0.1:8000/patients/self_aware?ids={ids_input}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            st.write("### Requested IDs:", data["requested_ids"])
            st.write("### Fetched Rows:")
            for row in data["rows"]:
                st.write(row)
        else:
            st.error(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
