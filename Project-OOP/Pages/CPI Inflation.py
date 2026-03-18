import streamlit as st
from models.dataset import Dataset
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart
from Visualization.pie_chart import PieChart

st.title("ASEAN CPI Inflation Dashboard")

dataset = Dataset("Datasets/asean_cpi_2000_2025.csv")
df = dataset.load()

if df is not None:

    st.subheader("Dataset Preview")
    st.dataframe(df)

    data = dataset.numeric()

    col1, col2 = st.columns(2)

    with col1:
        LineChart(data, "Inflation Trend").plot()

    with col2:
        BarChart(data, "Inflation Comparison").plot()

    PieChart(data, "Inflation Distribution").plot()