import matplotlib.pyplot as plt
from .base_chart import BaseChart


class AreaChart(BaseChart):
    def __init__(self, df, x: str, y: str,
                 title: str = "Area Chart",
                 figsize: tuple = (10, 5),
                 color: str = None):
        super().__init__(df, title, figsize)
        self.x     = x
        self.y     = y
        self.color = color or self.PALETTE[0]

    def plot(self) -> plt.Figure:
        fig, ax = self._make_fig()          # ← dark theme + grid + title

        data = self.df.sort_values(self.x)  # ← sort so line never zigzags

        r, g, b = (
            int(self.color[1:3], 16),
            int(self.color[3:5], 16),
            int(self.color[5:7], 16),
        )

        ax.fill_between(
            data[self.x], data[self.y],
            color=f"rgba({r},{g},{b},0.15)" if False else self.color,
            alpha=0.18,
            zorder=1,
        )
        ax.plot(
            data[self.x], data[self.y],
            color=self.color, linewidth=2, zorder=2,
        )

        ax.set_xlabel(self.x)
        ax.set_ylabel(self.y)
        fig.tight_layout()
        return fig                          # ← always return fig