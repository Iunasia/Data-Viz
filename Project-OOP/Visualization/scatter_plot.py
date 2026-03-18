import matplotlib.pyplot as plt
import streamlit as st
from Visualization.base_chart import BaseChart


class ScatterPlot(BaseChart):

    def plot(self):

        fig, ax = plt.subplots()

        columns = self.data.columns

        if len(columns) >= 2:
            ax.scatter(self.data[columns[0]], self.data[columns[1]])

        ax.set_title(self.title)

        st.pyplot(fig)