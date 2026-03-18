import streamlit as st
from models.dataset import Dataset
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart
from Visualization.pie_chart import PieChart

st.title("Data Science Salary Dashboard")

dataset = Dataset("Datasets/ds_salaries.csv")
df = dataset.load()

if df is not None:

    st.subheader("Dataset Preview")
    st.dataframe(df)

    data = dataset.numeric()

    col1, col2 = st.columns(2)

    with col1:
        LineChart(data, "Salary Trend").plot()

    with col2:
        BarChart(data, "Salary Comparison").plot()

    PieChart(data, "Salary Distribution").plot()