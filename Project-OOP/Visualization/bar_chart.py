import streamlit as st
import matplotlib.pyplot as plt


class BarChart:

    def __init__(self, data):
        self.data = data

    def plot(self, title="Bar Chart"):
        fig, ax = plt.subplots()

        self.data.plot(kind="bar", ax=ax)

        ax.set_title(title)
        ax.set_xlabel("Category")
        ax.set_ylabel("Value")

        st.pyplot(fig)