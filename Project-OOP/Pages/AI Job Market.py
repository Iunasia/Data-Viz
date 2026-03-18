import streamlit as st
from models.dataset import Dataset
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart
from Visualization.pie_chart import PieChart

st.title("AI Job Market Dashboard")

dataset = Dataset("Datasets/ai_jobs_market_2025_2026.csv")
df = dataset.load()

if df is not None:

    st.subheader("Dataset Preview")
    st.dataframe(df)

    data = dataset.numeric()

    col1, col2 = st.columns(2)

    with col1:
        LineChart(data, "AI Job Market Trend").plot()

    with col2:
        BarChart(data, "AI Job Market Comparison").plot()

    PieChart(data, "AI Job Market Distribution").plot()