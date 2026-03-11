import streamlit as st
import matplotlib.pyplot as plt


class BoxPlot:

    def __init__(self, data):
        self.data = data

    def plot(self, title="Box Plot"):
        fig, ax = plt.subplots()

        ax.boxplot(self.data)

        ax.set_title(title)

        st.pyplot(fig)