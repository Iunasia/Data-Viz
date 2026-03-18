import matplotlib.pyplot as plt
import streamlit as st
from Visualization.base_chart import BaseChart


class LineChart(BaseChart):

    def plot(self):

        fig, ax = plt.subplots()

        self.data.plot(ax=ax)

        ax.set_title(self.title)

        st.pyplot(fig)