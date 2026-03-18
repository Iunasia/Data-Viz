import streamlit as st
from models.dataset import Dataset
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart
from Visualization.pie_chart import PieChart

st.title("ASEAN GDP per Capita Dashboard")

dataset = Dataset("Datasets/asean_gdp_per_capita_2000_2025.csv")
df = dataset.load()

if df is not None:

    st.subheader("Dataset Preview")
    st.dataframe(df)

    data = dataset.numeric()

    col1, col2 = st.columns(2)

    with col1:
        LineChart(data, "GDP Trend").plot()

    with col2:
        BarChart(data, "GDP Comparison").plot()

    PieChart(data, "GDP Distribution").plot()