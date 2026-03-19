import matplotlib.pyplot as plt
from .base_chart import BaseChart


class HistogramChart(BaseChart):
    def __init__(self, df, column: str,
                 bins: int = 25,
                 group: str = None,
                 title: str = "Histogram",
                 figsize: tuple = (10, 5),
                 color: str = None):
        super().__init__(df, title, figsize)
        self.column = column
        self.bins   = bins
        self.group  = group
        self.color  = color or self.PALETTE[0]

    def plot(self) -> plt.Figure:
        fig, ax = self._make_fig()          # ← dark theme + grid + title

        if self.group:
            self._plot_grouped(ax)
        else:
            self._plot_single(ax)

        ax.set_xlabel(self.column)
        ax.set_ylabel("Count")             # ← was missing in original
        fig.tight_layout()
        return fig                         # ← always return fig

    # ── Single histogram ──────────────────────────────────────────────────────
    def _plot_single(self, ax):
        data = self.df[self.column].dropna()   # ← dropna prevents crash on NaN

        ax.hist(
            data,
            bins=self.bins,
            color=self.color,
            alpha=0.72,
            edgecolor="#fafafa",           # ← separates bars visually
            linewidth=0.5,
            zorder=2,
        )

    # ── Overlaid histograms, one per group ───────────────────────────────────
    def _plot_grouped(self, ax):
        groups = sorted(self.df[self.group].unique())

        for i, grp in enumerate(groups):
            data  = self.df[self.df[self.group] == grp][self.column].dropna()
            color = self.PALETTE[i % len(self.PALETTE)]

            ax.hist(
                data,
                bins=self.bins,
                label=str(grp),
                color=color,
                alpha=0.55,                # ← lower alpha so overlapping bars show through
                edgecolor="#f5f5f5",
                linewidth=0.4,
                zorder=2,
            )

        ax.legend(frameon=False, fontsize=9)