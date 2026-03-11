import pandas as pd
import os
import streamlit as st

class Dataset:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None

    def load(self):
        try:
            if not os.path.exists(self.file_path):
                raise FileNotFoundError(f"{self.file_path} not found")

            self.data = pd.read_csv(self.file_path)
            return self.data

        except Exception as e:
            st.error(f"Error loading dataset: {e}")
            return None