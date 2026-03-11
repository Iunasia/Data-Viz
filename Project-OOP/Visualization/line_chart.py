import streamlit as st
import matplotlib.pyplot as plt


class LineChart:

    def __init__(self, data):
        self.data = data

    def plot(self, title="Line Chart"):
        fig, ax = plt.subplots()

        self.data.plot(ax=ax)

        ax.set_title(title)
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")

        st.pyplot(fig)