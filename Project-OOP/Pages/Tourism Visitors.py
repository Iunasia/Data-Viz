import streamlit as st
import pandas as pd
from models.dataset import Dataset
from Visualization.area_chart import AreaChart
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart

st.set_page_config(page_title="Tourism Visitors", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; }
section[data-testid="stSidebar"] { background: #090c11 !important; }

.hero { padding: 40px 0 32px; border-bottom: 1px solid #1e2130; margin-bottom: 32px; }
.hero-tag { font-size: 11px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #34d399; margin-bottom: 12px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #f1f5f9; letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px; }
.hero-desc { font-size: 14px; font-weight: 300; color: #64748b; line-height: 1.7; max-width: 560px; }

.metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 36px; }
.metric-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 18px 20px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; color: #f1f5f9; line-height: 1; margin-bottom: 4px; }
.metric-label { font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-accent { color: #34d399; }

.chart-header { margin: 28px 0 6px; }
.chart-title { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.chart-desc { font-size: 12px; color: #475569; line-height: 1.5; }
.divider { height: 1px; background: #1e2130; margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── Load & reshape ────────────────────────────────────────────────────────────
raw = pd.read_csv("Datasets/visitor_asean.csv")

# Keep only total world visitors per destination country
total = raw[raw["Origin Country"] == "Total Country (World)"].copy()

# Reshape wide → long
df = total.melt(
    id_vars=["Destination Country"],
    value_vars=["2015", "2016", "2017", "2018", "2019", "2020"],
    var_name="year",
    value_name="visitors"
)
df.columns = ["country", "year", "visitors"]
df["year"]     = df["year"].astype(int)
df["visitors"] = pd.to_numeric(df["visitors"], errors="coerce")
df = df.dropna(subset=["visitors"])

# ── Stats ─────────────────────────────────────────────────────────────────────
total_visits  = int(df["visitors"].sum())
avg_visitors  = int(df["visitors"].mean())
top_country   = df.groupby("country")["visitors"].mean().idxmax()
peak_year     = int(df.groupby("year")["visitors"].sum().idxmax())
covid_drop    = int(df[df["year"] == 2019]["visitors"].sum())
covid_2020    = int(df[df["year"] == 2020]["visitors"].sum())
drop_pct      = round((1 - covid_2020 / covid_drop) * 100, 1)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Tourism · 2015 – 2020</div>
    <div class="hero-title">ASEAN Tourism Visitors</div>
    <div class="hero-desc">
        International visitor arrivals across
        <b style="color:#e2e8f0">{df['country'].nunique()} ASEAN destinations</b>
        from 2015 to 2020.
        <b style="color:#e2e8f0">{top_country}</b> is the top destination
        by average annual arrivals. COVID-19 caused a
        <b style="color:#e2e8f0">{drop_pct}%</b> drop in regional
        visitors from 2019 to 2020.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{df['country'].nunique()}</div>
        <div class="metric-label">Destinations</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">2015–2020</div>
        <div class="metric-label">Years covered</div>
    </div>
    <div class="metric-card">
        <div class="metric-value"><span class="metric-accent">{total_visits//1_000_000}M</span></div>
        <div class="metric-label">Total visitors</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{top_country}</div>
        <div class="metric-label">Top destination</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">-{drop_pct}%</div>
        <div class="metric-label">COVID-19 drop</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 1 ────────────────────────────────────────────────
st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Total Visitors by Country (Stacked)</div>
    <div class="chart-desc">
        Stacked area shows each country's contribution to total ASEAN arrivals.
        The sharp collapse in 2020 reflects the COVID-19 pandemic —
        a <b style="color:#e2e8f0">{drop_pct}%</b> drop from the 2019 peak.
    </div>
</div>
""", unsafe_allow_html=True)

df_area = df.groupby("year")["visitors"].sum().reset_index()
df_area.columns = ["year", "Total Visitors"]
AreaChart(df_area, x="year", y="Total Visitors",
         title="Total ASEAN Visitors Over Time").show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 2 ────────────────────────────────────────────────────────
df_bar = df.groupby("country")["visitors"].mean().reset_index()
df_bar = df_bar.sort_values("visitors", ascending=False)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Avg Annual Visitors by Destination</div>
    <div class="chart-desc">
        Countries ranked by average annual visitor arrivals 2015–2020.
        <b style="color:#e2e8f0">{top_country}</b> receives more
        visitors than the next two destinations combined.
    </div>
</div>
""", unsafe_allow_html=True)

BarChart(df_bar, x="country", y="visitors",
         title="Avg Annual Visitors by Country", horizontal=True).show(st)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:11px;color:#1e2130;text-align:center;">'
    'ASEAN Tourism Visitors · 2015–2020 · Project-OOP</p>',
    unsafe_allow_html=True
)