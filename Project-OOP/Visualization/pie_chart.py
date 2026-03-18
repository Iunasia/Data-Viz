import matplotlib.pyplot as plt
import streamlit as st
from Visualization.base_chart import BaseChart


class PieChart(BaseChart):

    def plot(self):

        fig, ax = plt.subplots()

        self.data.sum().plot(kind="pie", autopct="%1.1f%%", ax=ax)

        ax.set_ylabel("")
        ax.set_title(self.title)

        st.pyplot(fig)