import matplotlib.pyplot as plt
from .base_chart import BaseChart


class LineChart(BaseChart):
    def __init__(self, df, x: str, y: str,
                 group: str = None,
                 title: str = "Line Chart",
                 figsize: tuple = (10, 5),
                 color: str = None):
        super().__init__(df, title, figsize)
        self.x     = x
        self.y     = y
        self.group = group
        self.color = color or self.PALETTE[0]

    def plot(self) -> plt.Figure:
        fig, ax = self._make_fig()          # ← dark theme + grid + title

        if self.group:
            self._plot_grouped(ax)
        else:
            self._plot_single(ax)

        ax.set_xlabel(self.x)
        ax.set_ylabel(self.y)
        fig.tight_layout()
        return fig                          # ← always return fig

    # ── Single line ───────────────────────────────────────────────────────────
    def _plot_single(self, ax):
        data = self.df.sort_values(self.x)  # ← sort prevents zigzag line

        # Show markers only when few points — too many markers = crowded
        n       = len(data)
        marker  = "o" if n <= 20 else "none"
        msize   = 4  if n <= 20 else 0

        ax.plot(
            data[self.x], data[self.y],
            color=self.color,
            linewidth=2,
            marker=marker,
            markersize=msize,
            markerfacecolor=self.color,
            markeredgecolor="#0d1117",
            markeredgewidth=0.5,
        )

    # ── Multi-line: one line per group ────────────────────────────────────────
    def _plot_grouped(self, ax):
        groups = sorted(self.df[self.group].unique())

        for i, grp in enumerate(groups):
            sub   = self.df[self.df[self.group] == grp].sort_values(self.x)  # ← sort per group
            color = self.PALETTE[i % len(self.PALETTE)]
            n     = len(sub)

            # Suppress markers when many points per line — keeps chart clean
            marker = "o" if n <= 15 else "none"
            msize  = 3  if n <= 15 else 0

            ax.plot(
                sub[self.x], sub[self.y],
                label=str(grp),
                color=color,
                linewidth=2,
                marker=marker,
                markersize=msize,
                markerfacecolor=color,
                markeredgecolor="#0d1117",
                markeredgewidth=0.5,
            )

        # ← legend required — without it you can't tell which line is which country
        ax.legend(
            frameon=False,
            fontsize=9,
            loc="upper left",
            ncol=2 if len(groups) > 5 else 1,
        )