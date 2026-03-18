import matplotlib.pyplot as plt
import streamlit as st
from Visualization.base_chart import BaseChart


class Histogram(BaseChart):

    def plot(self):

        fig, ax = plt.subplots()

        self.data.plot(kind="hist", bins=20, ax=ax)

        ax.set_title(self.title)

        st.pyplot(fig)