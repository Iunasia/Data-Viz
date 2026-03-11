import streamlit as st
import matplotlib.pyplot as plt


class Histogram:

    def __init__(self, data):
        self.data = data

    def plot(self, title="Histogram"):
        fig, ax = plt.subplots()

        self.data.plot(kind="hist", bins=20, ax=ax)

        ax.set_title(title)
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")

        st.pyplot(fig)