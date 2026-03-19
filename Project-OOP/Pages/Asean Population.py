import streamlit as st
from models.dataset import Dataset
from Visualization.area_chart import AreaChart
from Visualization.line_chart import LineChart
from Visualization.bar_chart import BarChart

st.set_page_config(page_title="Population", layout="wide")

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #0d1117; }
section[data-testid="stSidebar"] { background: #090c11 !important; }

.hero { padding: 40px 0 32px; border-bottom: 1px solid #1e2130; margin-bottom: 32px; }
.hero-tag { font-size: 11px; font-weight: 500; letter-spacing: 0.18em; text-transform: uppercase; color: #f472b6; margin-bottom: 12px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 36px; font-weight: 800; color: #f1f5f9; letter-spacing: -1px; line-height: 1.1; margin-bottom: 12px; }
.hero-desc { font-size: 14px; font-weight: 300; color: #64748b; line-height: 1.7; max-width: 560px; }

.metric-row { display: grid; grid-template-columns: repeat(5, 1fr); gap: 12px; margin-bottom: 36px; }
.metric-card { background: #13151c; border: 1px solid #1e2130; border-radius: 12px; padding: 18px 20px; }
.metric-value { font-family: 'Syne', sans-serif; font-size: 24px; font-weight: 700; color: #f1f5f9; line-height: 1; margin-bottom: 4px; }
.metric-label { font-size: 11px; color: #475569; text-transform: uppercase; letter-spacing: 0.08em; }
.metric-accent { color: #f472b6; }

.chart-header { margin: 28px 0 6px; }
.chart-title { font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
.chart-desc { font-size: 12px; color: #475569; line-height: 1.5; }
.divider { height: 1px; background: #1e2130; margin: 28px 0; }
</style>
""", unsafe_allow_html=True)

# ── Load ──────────────────────────────────────────────────────────────────────
dataset = Dataset("Datasets/asean_population_2000_2026.csv")
dataset.load()
dataset.clean()
df = dataset.df

# ── Stats ─────────────────────────────────────────────────────────────────────
latest_year   = int(df["year"].max())
total_pop     = round(df[df["year"] == latest_year]["population_millions"].sum(), 1)
most_pop      = df.groupby("country")["population_millions"].mean().idxmax()
least_pop     = df.groupby("country")["population_millions"].mean().idxmin()
fastest       = (df.groupby("country")
                   .apply(lambda x: x.sort_values("year")["population_millions"].iloc[-1] /
                                    x.sort_values("year")["population_millions"].iloc[0])
                   .idxmax())

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="hero">
    <div class="hero-tag">Demographics · 2000 – {latest_year}</div>
    <div class="hero-title">ASEAN Population</div>
    <div class="hero-desc">
        Population trends across
        <b style="color:#e2e8f0">{df['country'].nunique()} ASEAN nations</b>
        from 2000 to {latest_year}.
        The region's total population reached
        <b style="color:#e2e8f0">{total_pop}M</b> in {latest_year},
        led by <b style="color:#e2e8f0">{most_pop}</b> as the most
        populous nation and <b style="color:#e2e8f0">{fastest}</b>
        as the fastest growing over the period.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Metric cards ──────────────────────────────────────────────────────────────
max_pop_country = df[df["year"] == latest_year].sort_values("population_millions", ascending=False).iloc[0]

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-value">{df['country'].nunique()}</div>
        <div class="metric-label">Countries</div>
    </div>
    <div class="metric-card">
        <div class="metric-value"><span class="metric-accent">{total_pop}M</span></div>
        <div class="metric-label">Total pop ({latest_year})</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{round(max_pop_country['population_millions'], 1)}M</div>
        <div class="metric-label">{most_pop} pop</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{latest_year - 2000} yrs</div>
        <div class="metric-label">Years covered</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{fastest}</div>
        <div class="metric-label">Fastest growing</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 1 ───────────────────────────────────────────────────────
df_total = df.groupby("year")["population_millions"].sum().reset_index()
df_total.columns = ["year", "Total Population (M)"]

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Total ASEAN Population Over Time</div>
    <div class="chart-desc">
        Combined population of all 10 ASEAN nations from 2000 to {latest_year}.
        The region has grown steadily, adding over
        <b style="color:#e2e8f0">
        {round(df_total['Total Population (M)'].iloc[-1] - df_total['Total Population (M)'].iloc[0], 1)}M
        </b> people over the period.
    </div>
</div>
""", unsafe_allow_html=True)

AreaChart(df_total, x="year", y="Total Population (M)",
          title="Total ASEAN Population Over Time").show(st)

st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# ── Chart 2 ────────────────────────────────────────────────────────
df_bar = df[df["year"] == latest_year].sort_values("population_millions", ascending=False)

st.markdown(f"""
<div class="chart-header">
    <div class="chart-title">Population Ranking ({latest_year})</div>
    <div class="chart-desc">
        Countries ranked by population in {latest_year}.
        <b style="color:#e2e8f0">{most_pop}</b> accounts for roughly
        <b style="color:#e2e8f0">
        {round(max_pop_country['population_millions'] / total_pop * 100)}%
        </b> of the total ASEAN population.
    </div>
</div>
""", unsafe_allow_html=True)

BarChart(df_bar, x="country", y="population_millions",
         title=f"Population by Country ({latest_year})", horizontal=True).show(st)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown(
    '<p style="font-size:11px;color:#1e2130;text-align:center;">'
    f'ASEAN Population · 2000–{latest_year} · Project-OOP</p>',
    unsafe_allow_html=True
)