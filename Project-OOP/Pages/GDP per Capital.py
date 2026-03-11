import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

country = st.sidebar.selectbox(
    "Select Country",
    ["Singapore", "Cambodia", "Malaysia", "Indonesia", "Myanmar", "Philippines", "Thailand", "Vietnam", "Brunei"]
)

year = st.sidebar.slider("Year", 2000, 2025)
