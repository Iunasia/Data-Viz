import streamlit as st
import pandas as pd

# Page configuration MUST be first
st.set_page_config(
    page_title="ASEAN Dashboard",
    layout="wide"
)

st.title("ASEAN Visitor Dashboard")

file_path = "./Data/visitor_asean.csv"

# File handling + error handling
try:
    df = pd.read_csv(file_path)

    st.subheader("Dataset Preview")
    st.dataframe(df)

    # Clean numeric data
    df = df.replace(',', '', regex=True)
    df = df.apply(pd.to_numeric, errors='ignore')

    numeric_df = df.select_dtypes(include='number')

    st.subheader("Visitors Trend")
    st.line_chart(numeric_df)

except FileNotFoundError:
    st.error("Dataset file not found.")
except Exception as e:
    st.error(f"Error loading dataset: {e}")

