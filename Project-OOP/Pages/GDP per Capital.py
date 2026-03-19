import streamlit as st
from models.dataset import Dataset
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart
from Visualization.area_chart import AreaChart

st.set_page_config(page_title="GDP per Capita", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; }
section[data-testid="stSidebar"] { background: #090c11 !important; }

.hero { padding: 40px 0 32px; border-bottom: 1px solid #1e2130; margin-bottom: 32px; }
.hero-tag { font-size: 11px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #a78bfa; margin-bottom: 12px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #f1f5f9; letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px; }
.hero-desc { font-size: 14px; font-weight: 300; color: #64748b; line-height: 1.7; max-width: 560px; }

.metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 36px; }
.metric-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 18px 20px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; color: #f1f5f9; line-height: 1; margin-bottom: 4px; }
.metric-label { font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-accent { color: #a78bfa; }

.chart-header { margin: 28px 0 6px; }
.chart-title { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.chart-desc { font-size: 12px; color: #475569; line-height: 1.5; }
.divider { height: 1px; background: #1e2130; margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── Load ──────────────────────────────────────────────────────────────────────
dataset = Dataset("Datasets/asean_gdp_per_capita_2000_2025.csv")
dataset.load()
dataset.clean()
df = dataset.df

# ── Stats ─────────────────────────────────────────────────────────────────────
avg_gdp      = int(df["gdp_per_capita_usd"].mean())
max_gdp      = int(df["gdp_per_capita_usd"].max())
richest      = df.groupby("country")["gdp_per_capita_usd"].mean().idxmax()
poorest      = df.groupby("country")["gdp_per_capita_usd"].mean().idxmin()
latest_year  = int(df["year"].max())
latest_sg    = int(df[(df["country"] == "Singapore") & (df["year"] == latest_year)]["gdp_per_capita_usd"].values[0])

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Economics · 2000 – {latest_year}</div>
    <div class="hero-title">ASEAN GDP per Capita</div>
    <div class="hero-desc">
        GDP per capita (USD) across
        <b style="color:#e2e8f0">{df['country'].nunique()} ASEAN nations</b>
        from 2000 to {latest_year}.
        <b style="color:#e2e8f0">{richest}</b> dominates the region
        with ${latest_sg:,} per capita in {latest_year}, while
        <b style="color:#e2e8f0">{poorest}</b> remains the lowest
        in average GDP per capita.
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
        <div class="metric-value"><span class="metric-accent">${avg_gdp:,}</span></div>
        <div class="metric-label">ASEAN avg GDP</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">${max_gdp//1000}k</div>
        <div class="metric-label">Highest recorded</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{richest}</div>
        <div class="metric-label">Richest country</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 1 ───────────────────────────────────────────────────────
df_avg = df.groupby("year")["gdp_per_capita_usd"].mean().reset_index()
df_avg.columns = ["year", "Avg GDP per Capita (USD)"]
peak_year = int(df_avg.loc[df_avg["Avg GDP per Capita (USD)"].idxmax(), "year"])

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">ASEAN Average GDP per Capita Trend</div>
    <div class="chart-desc">
        Regional average across all 10 countries per year.
        The ASEAN average reached its peak in
        <b style="color:#e2e8f0">{peak_year}</b>, driven by
        consistent growth in Singapore, Malaysia, and Thailand.
    </div>
</div>
""", unsafe_allow_html=True)

AreaChart(df_avg, x="year", y="Avg GDP per Capita (USD)",
          title="ASEAN Avg GDP per Capita Over Time").show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 2 ────────────────────────────────────────────────────────
df_bar = dataset.group_by("country", "gdp_per_capita_usd")
df_bar = df_bar.sort_values("gdp_per_capita_usd", ascending=False)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Avg GDP per Capita Ranking</div>
    <div class="chart-desc">
        Countries ranked by their 25-year average GDP per capita.
        <b style="color:#e2e8f0">{richest}</b> leads by a wide margin,
        followed by Brunei and Malaysia.
        <b style="color:#e2e8f0">{poorest}</b> sits at the bottom
        of the regional ranking.
    </div>
</div>
""", unsafe_allow_html=True)

BarChart(df_bar, x="country", y="gdp_per_capita_usd",
         title="Avg GDP per Capita by Country", horizontal=True).show(st)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:11px;color:#1e2130;text-align:center;">'
    f'ASEAN GDP per Capita · 2000–{latest_year} · Project-OOP</p>',
    unsafe_allow_html=True
)