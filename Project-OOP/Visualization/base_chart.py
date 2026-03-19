import matplotlib.pyplot as plt
import pandas as pd


# ── Shared dark theme (applied via rc_context — never pollutes global state) ──
_DARK_STYLE = {
    "figure.facecolor": "#0d1117",
    "axes.facecolor":   "#0d1117",
    "axes.edgecolor":   "#1e2130",
    "axes.labelcolor":  "#9ca3af",
    "xtick.color":      "#4b5563",
    "ytick.color":      "#4b5563",
    "grid.color":       "#1e2130",
    "text.color":       "#e8eaf0",
}

# ── Shared color palette (imported by every chart file) ───────────────────────
PALETTE = [
    "#6366f1", "#10b981", "#f59e0b", "#ef4444",
    "#3b82f6", "#ec4899", "#14b8a6", "#f97316",
]


class BaseChart:
    STYLE   = _DARK_STYLE
    PALETTE = PALETTE

    def __init__(self, df: pd.DataFrame, title: str = "Chart", figsize: tuple = (10, 5)):
        if df is None or df.empty:
            raise ValueError(
                f"{self.__class__.__name__}: DataFrame is empty or None."
            )
        self.df      = df
        self.title   = title
        self.figsize = figsize

    def _make_fig(self):
        """
        Create a pre-styled (fig, ax) pair.
        Call this at the top of every subclass plot() method.
        """
        with plt.rc_context(self.STYLE):
            fig, ax = plt.subplots(figsize=self.figsize)

        ax.set_title(self.title, color="#e8eaf0", fontsize=13, pad=14, loc="left")
        ax.grid(True, axis="y", linewidth=0.5, alpha=0.4)
        ax.spines[["top", "right", "left", "bottom"]].set_visible(False)
        return fig, ax

    def plot(self) -> plt.Figure:
        """
        Build and return a matplotlib Figure.
        Every subclass MUST override this and end with: return fig
        """
        raise NotImplementedError(
            f"{self.__class__.__name__} must implement plot() "
            "and return a matplotlib Figure."
        )

    def show(self, st):
        """Render the chart in a Streamlit app and close the figure to free memory."""
        fig = self.plot()
        if fig is None:
            raise ValueError(
                f"{self.__class__.__name__}.plot() returned None. "
                "Make sure plot() ends with 'return fig'."
            )
        st.pyplot(fig)
        plt.close(fig)

    def save(self, path: str, dpi: int = 150):
        """
        Export the chart to a file.
        Format is inferred from the extension: .png  .pdf  .svg

        Example:
            chart.save("output/salary_chart.png")
            chart.save("report.pdf", dpi=300)
        """
        fig = self.plot()
        fig.savefig(path, dpi=dpi, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        plt.close(fig)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"title={self.title!r}, "
            f"rows={len(self.df)}, "
            f"figsize={self.figsize})"
        )