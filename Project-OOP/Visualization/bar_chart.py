import matplotlib.pyplot as plt
import streamlit as st
from Visualization.base_chart import BaseChart


class BarChart(BaseChart):

    def plot(self):

        fig, ax = plt.subplots()

        self.data.plot(kind="bar", ax=ax)

        ax.set_title(self.title)

        st.pyplot(fig)