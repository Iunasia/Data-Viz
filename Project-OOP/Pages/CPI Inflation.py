import streamlit as st
from models.dataset import Dataset
from Visualization.area_chart import AreaChart
from Visualization.bar_chart import BarChart
from Visualization.histogram import HistogramChart

st.set_page_config(page_title="CPI Inflation", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; }
section[data-testid="stSidebar"] { background: #090c11 !important; }

.hero { padding: 40px 0 32px; border-bottom: 1px solid #1e2130; margin-bottom: 32px; }
.hero-tag { font-size: 11px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #f59e0b; margin-bottom: 12px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #f1f5f9; letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px; }
.hero-desc { font-size: 14px; font-weight: 300; color: #64748b; line-height: 1.7; max-width: 560px; }

.metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 36px; }
.metric-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 18px 20px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; color: #f1f5f9; line-height: 1; margin-bottom: 4px; }
.metric-label { font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-accent { color: #f59e0b; }

.chart-header { margin: 28px 0 6px; }
.chart-title { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.chart-desc { font-size: 12px; color: #475569; line-height: 1.5; }
.divider { height: 1px; background: #1e2130; margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── Load ──────────────────────────────────────────────────────────────────────
dataset = Dataset("Datasets/asean_cpi_2000_2025.csv")
dataset.load()
dataset.clean()
df = dataset.df

# ── Stats ─────────────────────────────────────────────────────────────────────
avg_cpi      = round(df["cpi_inflation_percent"].mean(), 2)
max_cpi      = round(df["cpi_inflation_percent"].max(), 2)
min_cpi      = round(df["cpi_inflation_percent"].min(), 2)
highest_ctry = df.groupby("country")["cpi_inflation_percent"].mean().idxmax()
lowest_ctry  = df.groupby("country")["cpi_inflation_percent"].mean().idxmin()

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Economics · 2000 – 2025</div>
    <div class="hero-title">ASEAN CPI Inflation</div>
    <div class="hero-desc">
        Tracks Consumer Price Index inflation across
        <b style="color:#e2e8f0">{df['country'].nunique()} ASEAN nations</b>
        over {df['year'].nunique()} years.
        <b style="color:#e2e8f0">{highest_ctry}</b> has the highest average
        inflation while <b style="color:#e2e8f0">{lowest_ctry}</b> remains
        the most stable economy in the region.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{df['country'].nunique()}</div>
        <div class="metric-label">Countries</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{df['year'].nunique()}</div>
        <div class="metric-label">Years covered</div>
    </div>
    <div class="metric-card">
        <div class="metric-value"><span class="metric-accent">{avg_cpi}%</span></div>
        <div class="metric-label">ASEAN avg CPI</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{max_cpi}%</div>
        <div class="metric-label">Highest recorded</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{min_cpi}%</div>
        <div class="metric-label">Lowest recorded</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 1 ───────────────────────────────────────────────────────
df_avg = df.groupby("year")["cpi_inflation_percent"].mean().reset_index()
df_avg.columns = ["year", "avg_cpi"]
peak_year = int(df_avg.loc[df_avg["avg_cpi"].idxmax(), "year"])

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">ASEAN Average CPI Inflation Trend</div>
    <div class="chart-desc">
        Average inflation across all 10 ASEAN countries per year.
        The region peaked in <b style="color:#e2e8f0">{peak_year}</b> —
        visible as the highest point on the area chart.
    </div>
</div>
""", unsafe_allow_html=True)

AreaChart(df_avg, x="year", y="avg_cpi",
          title="ASEAN Avg CPI Inflation % Over Time").show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 2 ────────────────────────────────────────────────────────
df_bar = dataset.group_by("country", "cpi_inflation_percent")
df_bar = df_bar.sort_values("cpi_inflation_percent", ascending=False)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Avg CPI Inflation by Country</div>
    <div class="chart-desc">
        Country-level average inflation over the full 2000–2025 period.
        <b style="color:#e2e8f0">{highest_ctry}</b> leads the region
        while <b style="color:#e2e8f0">{lowest_ctry}</b> has maintained
        the lowest average inflation.
    </div>
</div>
""", unsafe_allow_html=True)

BarChart(df_bar, x="country", y="cpi_inflation_percent",
         title="Avg CPI Inflation by Country", horizontal=True).show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)