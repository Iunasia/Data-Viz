import streamlit as st
import matplotlib.pyplot as plt


class ScatterPlot:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def plot(self, title="Scatter Plot"):
        fig, ax = plt.subplots()

        ax.scatter(self.x, self.y)

        ax.set_title(title)
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        st.pyplot(fig)