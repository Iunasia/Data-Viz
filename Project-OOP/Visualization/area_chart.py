import streamlit as st
import matplotlib.pyplot as plt


class AreaChart:

    def __init__(self, data):
        self.data = data

    def plot(self, title="Area Chart"):
        fig, ax = plt.subplots()

        self.data.plot.area(ax=ax)

        ax.set_title(title)
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")

        st.pyplot(fig)