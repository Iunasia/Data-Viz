import pandas as pd

class Dataset:
    def __init__(self, path):
        self.path = path
        self.df = None

    def load(self):
        try:
            self.df = pd.read_csv(self.path)
            return self.df
        except Exception as e:
            print("Error loading dataset:", e)
            return None

    def clean(self):
        self.df.columns = self.df.columns.str.strip().str.lower().str.replace(" ", "_")
        return self.df

    def group_by(self, column, value, agg="mean"):
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        if value not in self.df.columns:
            raise ValueError(f"Column '{value}' not found")

        return (
            self.df.groupby(column)[value]
            .agg(agg)
            .reset_index()
        )

    def value_counts(self, column):
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found")

        df = self.df[column].value_counts().reset_index()
        df.columns = [column, "count"]
        return df