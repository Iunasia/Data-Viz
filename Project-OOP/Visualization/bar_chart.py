import matplotlib.pyplot as plt
from .base_chart import BaseChart


class BarChart(BaseChart):
    def __init__(self, df, x: str, y: str,
                 title: str = "Bar Chart",
                 figsize: tuple = (10, 5),
                 color: str = None,
                 horizontal: bool = False):
        super().__init__(df, title, figsize)
        self.x          = x
        self.y          = y
        self.color      = color or self.PALETTE[0]
        self.horizontal = horizontal

    def plot(self) -> plt.Figure:
        fig, ax = self._make_fig()          # ← dark theme + grid + title

        if self.horizontal:
            self._plot_horizontal(ax)
        else:
            self._plot_vertical(ax)

        fig.tight_layout()
        return fig                          # ← always return fig

    # ── Vertical bars ─────────────────────────────────────────────────────────
    def _plot_vertical(self, ax):
        bars = ax.bar(
            self.df[self.x], self.df[self.y],
            color=self.color, width=0.6, zorder=2,
        )

        # Value labels above each bar
        for bar in bars:
            h = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                h * 1.01,
                f"{h:,.0f}",
                ha="center", va="bottom",
                fontsize=9, color="#9ca3af",
            )

        # ← ax.tick_params() is scoped to this axes only
        #   Your original used plt.xticks() which is global state
        #   and rotates ticks on ALL currently open figures
        ax.tick_params(axis="x", rotation=45)
        ax.set_xlabel(self.x)
        ax.set_ylabel(self.y)

    # ── Horizontal bars ───────────────────────────────────────────────────────
    def _plot_horizontal(self, ax):
        # Sort ascending so largest bar is at the top
        data = self.df.sort_values(self.y, ascending=True)

        bars = ax.barh(
            data[self.x], data[self.y],
            color=self.color, height=0.6, zorder=2,
        )

        # Value labels beside each bar
        for bar in bars:
            w = bar.get_width()
            ax.text(
                w * 1.01, bar.get_y() + bar.get_height() / 2,
                f"{w:,.0f}",
                ha="left", va="center",
                fontsize=9, color="#9ca3af",
            )

        # Turn off y-grid, use x-grid for horizontal bars
        ax.grid(True, axis="x", linewidth=0.5, alpha=0.4)
        ax.grid(False, axis="y")
        ax.set_xlabel(self.y)
        ax.set_ylabel(self.x)