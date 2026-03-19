import matplotlib.pyplot as plt
from .base_chart import BaseChart


class PieChart(BaseChart):
    def __init__(self, df, labels: str, values: str,
                 title: str = "Pie Chart",
                 figsize: tuple = (7, 5),
                 donut: bool = True):
        super().__init__(df, title, figsize)
        self.labels = labels
        self.values = values
        self.donut  = donut

    def plot(self) -> plt.Figure:
        fig, ax = self._make_fig()          # ← dark theme + grid + title

        # Build slice colors from PALETTE — cycles if more slices than colors
        n_slices = len(self.df)
        colors   = [self.PALETTE[i % len(self.PALETTE)] for i in range(n_slices)]

        wedge_props = dict(
            edgecolor="#0d1117",            # ← dark edge separates slices
            linewidth=1.5,
        )
        if self.donut:
            wedge_props["width"] = 0.55     # ← donut hole (0 = full pie, 1 = ring)

        wedges, texts, autotexts = ax.pie(
            self.df[self.values],
            labels=self.df[self.labels],
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,                 # ← first slice at top, looks balanced
            pctdistance=0.75,              # ← % label sits inside the donut band
            wedgeprops=wedge_props,
            textprops=dict(
                color="#9ca3af",           # ← muted light color — readable on dark bg
                fontsize=10,
            ),
        )

        # % labels need slightly brighter color to stand out from slice labels
        for autotext in autotexts:
            autotext.set_color("#e8eaf0")
            autotext.set_fontsize(9)

        ax.set_aspect("equal")
        fig.tight_layout()
        return fig                         # ← always return fig