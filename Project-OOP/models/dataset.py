import pandas as pd
import streamlit as st


class Dataset:

    def __init__(self, path):
        self.path = path
        self.data = None

    def load(self):
        try:
            self.data = pd.read_csv(self.path)
            return self.data
        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None

    def numeric(self):
        if self.data is not None:
            return self.data.select_dtypes(include="number")
        return None